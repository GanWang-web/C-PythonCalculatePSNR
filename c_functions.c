#include "c_functions.h"
#include <stdio.h>

void make_coloured_image(int* red, int* green, int* blue, int len, struct ColouredPixels* cp, union PixelData* pd, struct Image* im) {
    cp->red = red;
    cp->green = green;
    cp->blue = blue;
    pd->colour_pixels = *cp;
    im->pd = *pd;
    im->length = len;
    im->is_coloured = 1;
}

void make_monochrome_image(int* grey, int len, union PixelData* pd, struct Image* im) {
    pd->grey_pixels = grey;
    im->pd = *pd;
    im->length = len;
    im->is_coloured = 0;
}

float c_r_psnr_wrapper(int* red1, int* green1, int* blue1, int* red2, int* green2, int* blue2, int len) {
    struct ColouredPixels cp1;
    struct ColouredPixels cp2;

    union PixelData pd1;
    union PixelData pd2;

    struct Image image1;
    struct Image image2;

    make_coloured_image(red1, green1, blue1, len, &cp1, &pd1, &image1);
    make_coloured_image(red2, green2, blue2, len, &cp2, &pd2, &image2);
    
    return c_r_psnr(&image1, &image2);
}

float c_g_psnr_wrapper(int* red1, int* green1, int* blue1, int* red2, int* green2, int* blue2, int len) {
    struct ColouredPixels cp1;
    struct ColouredPixels cp2;

    union PixelData pd1;
    union PixelData pd2;

    struct Image image1;
    struct Image image2;

    make_coloured_image(red1, green1, blue1, len, &cp1, &pd1, &image1);
    make_coloured_image(red2, green2, blue2, len, &cp2, &pd2, &image2);
    
    return c_g_psnr(&image1, &image2);
}

float c_b_psnr_wrapper(int* red1, int* green1, int* blue1, int* red2, int* green2, int* blue2, int len) {
    struct ColouredPixels cp1;
    struct ColouredPixels cp2;

    union PixelData pd1;
    union PixelData pd2;

    struct Image image1;
    struct Image image2;

    make_coloured_image(red1, green1, blue1, len, &cp1, &pd1, &image1);
    make_coloured_image(red2, green2, blue2, len, &cp2, &pd2, &image2);
    
    return c_b_psnr(&image1, &image2);
}

float c_total_psnr_wrapper(int* red1, int* green1, int* blue1, int* red2, int* green2, int* blue2, int len, int is_coloured) {
    struct ColouredPixels cp1;
    struct ColouredPixels cp2;

    union PixelData pd1;
    union PixelData pd2;

    struct Image image1;
    struct Image image2;

    if (is_coloured) {
        make_coloured_image(red1, green1, blue1, len, &cp1, &pd1, &image1);
        make_coloured_image(red2, green2, blue2, len, &cp2, &pd2, &image2);
    } else {
        make_monochrome_image(red1, len, &pd1, &image1);
        make_monochrome_image(red2, len, &pd2, &image2);
    }
    float f = c_total_psnr(&image1, &image2);
    return f;
}

float PSNR_calculation(float MSE)
{
    double PSNR = 0;
    if (MSE == 0)
    {
        return PSNR;
    }
    else
    {
        PSNR = 10 * log10(pow(255, 2) / MSE);
    }
    return PSNR;
}

float MSE_calculation(int *I1, int *I2, int length)
{
    double MSE, difference_pow, difference_pow_total;
    MSE = difference_pow = difference_pow_total = 0;
    for (int i = 0; i < length; i++)
    {
        difference_pow = pow(I1[i] - I2[i], 2);
        difference_pow_total += difference_pow;
    };
    MSE = difference_pow_total / length;
    return MSE;
}

float c_r_psnr(struct Image *image1, struct Image *image2)
{
    //TODO
    int *I1, *I2;
    double MSE = 0;
    I1 = (int *)image1->pd.colour_pixels.red;
    I2 = (int *)image2->pd.colour_pixels.red;
    MSE = MSE_calculation(I1, I2, image1->length);
    return PSNR_calculation(MSE);
}

float c_g_psnr(struct Image *image1, struct Image *image2)
{
    //TODO
    int *I1, *I2;
    double MSE = 0;
    I1 = (int *)image1->pd.colour_pixels.green;
    I2 = (int *)image2->pd.colour_pixels.green;
    MSE = MSE_calculation(I1, I2, image1->length);
    return PSNR_calculation(MSE);
}

float c_b_psnr(struct Image *image1, struct Image *image2)
{
    //TODO
    int *I1, *I2;
    double MSE = 0;
    I1 = (int *)image1->pd.colour_pixels.blue;
    I2 = (int *)image2->pd.colour_pixels.blue;
    MSE = MSE_calculation(I1, I2, image1->length);
    return PSNR_calculation(MSE);
}

float c_total_psnr(struct Image *image1, struct Image *image2)
{
    //TODO
    if (image1->is_coloured == 0)
    {
        double MSE = 0;
        int *I1, *I2;
        I1 = (int *)image1->pd.grey_pixels;
        I2 = (int *)image2->pd.grey_pixels;
        MSE = MSE_calculation(I1, I2, image1->length);
        return PSNR_calculation(MSE);
    }
    else
    {
        double red_MSE, blue_MSE, green_MSE, MSE_all;
        red_MSE = blue_MSE = green_MSE = MSE_all = 0;
        int *I1_r, *I1_g, *I1_b, *I2_r, *I2_g, *I2_b;
        I1_r = (int *)image1->pd.colour_pixels.red;
        I1_g = (int *)image1->pd.colour_pixels.green;
        I1_b = (int *)image1->pd.colour_pixels.blue;
        I2_r = (int *)image2->pd.colour_pixels.red;
        I2_g = (int *)image2->pd.colour_pixels.green;
        I2_b = (int *)image2->pd.colour_pixels.blue;
        red_MSE = MSE_calculation(I1_r, I2_r, image1->length);
        green_MSE = MSE_calculation(I1_g, I2_g, image1->length);
        blue_MSE = MSE_calculation(I1_b, I2_b, image1->length);
        MSE_all = (red_MSE + green_MSE + blue_MSE) / 3;
        return PSNR_calculation(MSE_all);
    }
}