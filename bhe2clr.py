import numpy as np
import cv2
import matplotlib.pyplot as plt

img = cv2.imread('134008.jpg')
img = cv2.resize(img, (256, 256))
cv2.imshow('Input Image', img)

b, g, r = cv2.split(img)

def bi_histogram_equalization_sd(channel):
    mean_val = np.mean(channel)
    std_dev = np.std(channel)
    
    lower_bound = mean_val - std_dev
    upper_bound = mean_val + std_dev
    
    low_part = channel[channel <= lower_bound]
    high_part = channel[channel > lower_bound]
    
    freq_low = np.zeros(256)
    freq_high = np.zeros(256)
    
    for i in range(low_part.shape[0]):
        freq_low[low_part[i]] += 1
    
    for i in range(high_part.shape[0]):
        freq_high[high_part[i]] += 1
    
    plt.plot(np.arange(256), freq_low, color='blue')
    plt.grid(True)
    plt.show()
    
    plt.plot(np.arange(256), freq_high, color='red')
    plt.grid(True)
    plt.show()
    
    pdf_low = freq_low / low_part.size
    pdf_high = freq_high / high_part.size
    
    cdf_low = np.zeros(256)
    cdf_high = np.zeros(256)
    
    cdf_low[0] = pdf_low[0]
    cdf_high[0] = pdf_high[0]
    
    for i in range(1, 256):
        cdf_low[i] = cdf_low[i - 1] + pdf_low[i]
        cdf_high[i] = cdf_high[i - 1] + pdf_high[i]
    
    cdf_low = cdf_low * lower_bound
    cdf_high = (cdf_high * (255 - lower_bound)) + lower_bound
    
    better_channel = np.zeros_like(channel)
    
    for i in range(256):
        for j in range(256):
            if channel[i, j] <= lower_bound:
                better_channel[i, j] = cdf_low[channel[i, j]]
            else:
                better_channel[i, j] = cdf_high[channel[i, j]]
    
    return better_channel

better_b = bi_histogram_equalization_sd(b)
better_g = bi_histogram_equalization_sd(g)
better_r = bi_histogram_equalization_sd(r)

better_img = cv2.merge((better_b, better_g, better_r))

cv2.imwrite('134008.jpg', better_img)
cv2.imshow('Better Image', better_img)
cv2.waitKey(0)
cv2.destroyAllWindows()
