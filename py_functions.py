import math

def PSNR_calculation(MSE):
    if(MSE == 0):
        PSNR = 0.0
    else:
        PSNR = 10*math.log10(255**2/MSE)
    return PSNR


def MSE_calculation(image1, image2, color):
    MSE = difference_pow_total = 0.0
    if(color == "red"):
        pixel_column = 0
    elif(color == "green"):
        pixel_column = 1
    elif(color == "blue"):
        pixel_column = 2
    i = 0
    while i < len(image1):
        difference_pow = math.pow(
            (image1[i][pixel_column]-image2[i][pixel_column]), 2)
        difference_pow_total += difference_pow
        i = i+1
    MSE = difference_pow_total/len(image1)
    return MSE


def py_r_psnr(image1, image2):
    MSE = MSE_calculation(image1, image2, "red")
    return PSNR_calculation(MSE)


def py_g_psnr(image1, image2):
    MSE = MSE_calculation(image1, image2, "green")
    return PSNR_calculation(MSE)


def py_b_psnr(image1, image2):
    MSE = MSE_calculation(image1, image2, "blue")
    return PSNR_calculation(MSE)


def py_total_psnr(image1, image2):
    if(len(image1[0]) == 1 and len(image2[0]) == 1):
        MSE = MSE_calculation(image1, image2, "red")
        return PSNR_calculation(MSE)
    else:
        red_MSE = MSE_calculation(image1, image2, "red")
        green_MSE = MSE_calculation(image1, image2, "green")
        blue_MSE = MSE_calculation(image1, image2, "blue")
        total_MSE = (red_MSE+green_MSE+blue_MSE)/3
        return PSNR_calculation(total_MSE)
