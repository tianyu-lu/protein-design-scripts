import torch
import torch.nn as nn
from torch.optim import Adam
import numpy as np
import glob
import matplotlib.pyplot as plt

dataset = np.array(glob.glob("data/*.npy"))
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
# device = torch.device("cpu")
# torch.cuda.set_device(0)
# torch.ones(5,5).cuda()
# torch.ones(5,5).to(device)

def generate_real_samples(n_samples):
  # choose random instances
  ix = np.random.randint(0, len(dataset), n_samples)
  # retrieve selected images
  X_names = dataset[ix]
  X = []
  for x in X_names:
    X.append(np.load(x, allow_pickle=True))
  X = np.array(X)
  # generate 'real' class labels (1)
  y = torch.ones(n_samples, 1)
  b, w, h = X.shape
  X_pad = np.zeros((b, w+2, h+2))
  X_pad[:,1:-1, 1:-1] += X
  X = X_pad.reshape(b, 1, w+2, h+2)
  X = torch.from_numpy(X).type(torch.float32)
  return X.to(device), y.to(device)

def generate_fake_samples(G, latent_dim, n_samples):
  # generate points in latent space
  z = torch.randn(n_samples, latent_dim).to(device)
  # predict outputs
  X = G(z)
  # create 'fake' class labels (0)
  y = torch.zeros(5,5)
  y = torch.zeros(int(n_samples), 1)
  return X.to(device), y.to(device)

# create and save a plot of generated images
def save_plot(examples, epoch, n=7):
  # plot images
  for i in range(4):
    # define subplot
    plt.subplot(2, 2, 1 + i)
    # turn off axis
    plt.axis('off')
    # plot raw pixel data
    img = examples[i].detach().cpu().squeeze()
    np.save("{}-{}.npy".format(epoch+1, i), np.array(img))
    plt.imshow(img)
  # save plot to file
  filename = 'generated_plot_e%03d.png' % (epoch+1)
  plt.savefig(filename)
  plt.close()

# evaluate the discriminator, plot generated images, save generator model
def summarize_performance(epoch, G, D, latent_dim, n_samples=150):
  G.eval()
  D.eval()
  # prepare real samples
  # X_real, y_real = generate_real_samples(n_samples)
  # # evaluate discriminator on real examples
  # _, acc_real = D(X_real, y_real, verbose=0)
  # prepare fake examples
  x_fake, y_fake = generate_fake_samples(G, latent_dim, n_samples)
  # evaluate discriminator on fake examples
  # _, acc_fake = D(x_fake, y_fake, verbose=0)
  # # summarize discriminator performance
  # print('>Accuracy real: %.0f%%, fake: %.0f%%' % (acc_real*100, acc_fake*100))
  # save plot
  save_plot(x_fake, epoch)

class Generator(nn.Module):
  def __init__(self):
    super(Generator, self).__init__()
    self.fc = nn.Linear(1024, 512*2*2)
    self.upsample = nn.Sequential(
                        nn.ConvTranspose2d(512, 256, 4, stride=4, padding=0),
                        nn.BatchNorm2d(256),
                        nn.LeakyReLU(0.2),
                        nn.ConvTranspose2d(256, 128, 4, stride=4, padding=0),
                        nn.BatchNorm2d(128),
                        nn.LeakyReLU(0.2),
                        nn.ConvTranspose2d(128, 64, 4, stride=2, padding=1),
                        nn.BatchNorm2d(64),
                        nn.LeakyReLU(0.2),
                        nn.ConvTranspose2d(64, 1, 4, stride=2, padding=1)
                    )
  def forward(self, z):
    out = self.fc(z).reshape(-1, 512, 2, 2)
    out = self.upsample(out)
    out = torch.clamp(out, min=0.0)
    out = (out + out.permute(0,1,3,2)) / 2
    return out

class Discriminator(nn.Module):
  def __init__(self):
    super(Discriminator, self).__init__()
    self.D = nn.Sequential(
                  nn.Conv2d(1, 64, 4, stride=2, padding=1),
                  nn.LeakyReLU(0.2),
                  nn.Dropout2d(0.1),
                  nn.Conv2d(64, 128, 4, stride=2, padding=1),
                  nn.BatchNorm2d(128),
                  nn.LeakyReLU(0.2),
                  nn.Dropout2d(0.1),
                  nn.Conv2d(128, 256, 4, stride=4, padding=0),
                  nn.BatchNorm2d(256),
                  nn.LeakyReLU(0.2),
                  nn.Dropout2d(0.1),
                  nn.Conv2d(256, 512, 4, stride=2, padding=1),
                  nn.BatchNorm2d(512),
                  nn.LeakyReLU(0.2),
                  nn.Dropout2d(0.1),
                  nn.Conv2d(512, 1, 4, stride=1, padding=0),
                  nn.Sigmoid()
              )
  def forward(self, img):
    return self.D(img)

class GAN(nn.Module):
  def __init__(self, G, D):
    super(GAN, self).__init__()
    self.G = G
    self.D = D

  def forward(self, z):
    for param in self.D.parameters():
      param.requires_grad = False
    return self.D(self.G(z))

import random
seed_val = 777
random.seed(seed_val)
np.random.seed(seed_val)
torch.manual_seed(seed_val)
torch.cuda.manual_seed_all(seed_val)

loss_fn = nn.BCELoss()

class MyDataParallel(nn.DataParallel):
  """
  Allow nn.DataParallel to call model's attributes.
  """
  def __getattr__(self, name):
    try:
      return super().__getattr__(name)
    except AttributeError:
      return getattr(self.module, name)

G = Generator().to(device)
D = Discriminator().to(device)
D_G = GAN(G, D).to(device)

# X_fake, y_fake = generate_fake_samples(G, 1024, 4)

D_optimizer = Adam(D.parameters(), lr=1e-5, betas=(0.5, 0.999))
G_optimizer = Adam(D_G.parameters(), lr=7.5e-5, betas=(0.5, 0.999))
lmbd = lambda x: x / 10
D_scheduler = torch.optim.lr_scheduler.LambdaLR(D_optimizer, lr_lambda=lmbd)
G_scheduler = torch.optim.lr_scheduler.LambdaLR(G_optimizer, lr_lambda=lmbd)

def train(D, D_G, latent_dim, n_epochs=200, n_batch=8):
  bat_per_epo = int(len(dataset) / n_batch)
  half_batch = int(n_batch / 2)
  best_g_loss = 1e7
  curr_iter = 1
  # manually enumerate epochs
  for i in range(n_epochs):
    # enumerate batches over the training set
    for j in range(bat_per_epo):
      curr_iter += 1
      D.train()
      for param in D.parameters():
        param.requires_grad = True
      D_G.train()
      # get randomly selected 'real' samples
      X_real, y_real = generate_real_samples(half_batch)
      # update discriminator model weights
      D_preds = D(X_real)
      D_loss_real = loss_fn(D_preds.reshape(-1,1), y_real)
      D_optimizer.zero_grad()
      D_loss_real.backward()
      D_optimizer.step()
      # generate 'fake' examples
      X_fake, y_fake = generate_fake_samples(G, latent_dim, half_batch)
      # update discriminator model weights
      D_preds = D(X_fake)
      D_loss_fake = loss_fn(D_preds.reshape(-1,1), y_fake)
      D_optimizer.zero_grad()
      D_loss_fake.backward()
      D_optimizer.step()
      # prepare points in latent space as input for the generator
      z = torch.randn(n_batch, latent_dim).to(device)
      # create inverted labels for the fake samples
      y_gan = torch.ones(n_batch, 1).to(device)
      # update the generator via the discriminator's error
      D_G_preds = D_G(z)
      D_G_loss = loss_fn(D_G_preds.reshape(-1,1).to(device), y_gan)
      G_optimizer.zero_grad()
      D_G_loss.backward()
      G_optimizer.step()
      if curr_iter % 12500 == 0:
        D_scheduler.step()
        G_scheduler.step()
      # summarize loss on this batch
      if (j+1)%1000 == 0:
        print('>%d, %d/%d, d1=%.3f, d2=%.3f g=%.3f' %
        (i+1, j+1, bat_per_epo, D_loss_real.cpu().item(), D_loss_fake.cpu().item(), D_G_loss.cpu().item()), flush=True)

        summarize_performance((i+1)*j, G, D, latent_dim)
      if D_G_loss.cpu().item() < best_g_loss:
        best_g_loss = D_G_loss.cpu().item()
        filename = 'generator_model_%03d.h5' % (j+1)
        torch.save(G.state_dict(), filename)
    # evaluate the model performance, sometimes
    if (i+1) % 10 == 0:
      summarize_performance(i, G, D, latent_dim)

# size of the latent space
latent_dim = 1024

# train model
train(D, D_G, latent_dim)
