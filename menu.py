import py_functions
import translation
import sys
import os.path

images = []
Python = True


def deal_show():
  if(images == []):
    print("No loaded images to show.")
    goto_begining()
  else:
    print("Loaded images:")
    i = 0
    while i < len(images):
      colour_mono = "colour."
      pixel_arr_length = len(images[i][0])
      if(pixel_arr_length == 1):
        colour_mono = "monochrome."
      print("Image %d, Length %d, %s" % (i+1, len(images[i]), colour_mono))
      i = i+1
  goto_begining()


def check_pixel_arr(whole_img):
  for i in whole_img:
    if(len(i) != 3 and len(i) != 1):
      print("Error: Image does not appear in RGB or monochrome format.")
      goto_begining()


def check_num_range(num):
  try:
    int(num)
  except ValueError:
    print("Error: Non-integer value found in image file.")
    goto_begining()
  if(int(num) < 0 or int(num) > 255):
    print("Error: Number outside the range of 0 to 255 found in image file.")
    goto_begining()


def check_file(f):
  if(os.path.exists(f) == False):
    print("Error: File does not exist.")
    goto_begining()
  elif(os.path.getsize(f) == 0):
    print("Error: File is empty.")
    goto_begining()


def deal_load():
  whole_img = []
  f = input("Enter the filename you want to load: ")
  res = check_file(f)
  f = open(f)
  line = f.readline()
  while line:
    pixel_arr = list(line.rstrip("\n").split(","))
    for i in pixel_arr:
      check_num_range(i)
      pixel_arr[pixel_arr.index(i)] = int(i)
    whole_img.append(pixel_arr)
    line = f.readline()
  f.close()
  check_pixel_arr(whole_img)
  images.append(whole_img)
  goto_begining()


def deal_photo_index(index):
  if(len(index) == 2):
    return index
  else:
    photo_selection = input(
        "What is the index of the image you would like to select? ")
    try:
      photo_selection = int(photo_selection)-1
      if(photo_selection < 0 or photo_selection > len(images)-1):
        print("The index should be between 1 and %d." % (len(images)))
        return deal_photo_index(index)
    except ValueError:
      print("That is not a valid integer.")
      return deal_photo_index(index)
  index.append(photo_selection)
  return deal_photo_index(index)


def check_comparable(index, color):
  selected_img1 = images[index[0]]
  selected_img2 = images[index[1]]
  if((len(selected_img1[0]) == 1 or len(selected_img2[0]) == 1) and color != "PSNR"):
    print("One of those images is not in colour; cannot compute %s PSNR." % color)
    goto_begining()
  elif(len(selected_img1[0]) != len(selected_img2[0])):
    print("Images are not the same type; cannot compute PSNR between them.")
    goto_begining()
  elif(len(selected_img1) != len(selected_img2)):
    print("Images are not the same length; cannot compute PSNR between them.")
    goto_begining()


def deal_PSNR(command):
  color = 'PSNR'
  if(command == "PSNR-R"):
    color = "red"
  elif(command == "PSNR-G"):
    color = "green"
  elif(command == "PSNR-B"):
    color = "blue"
  if(images == []):
    print("No images have been loaded. No image can be selected.")
    goto_begining()
  else:
    index = deal_photo_index([])
    check_comparable(index, color)
    calculate_PSNR(command, index)


def calculate_PSNR(command, index):
  PSNR = 0
  img1 = images[int(index[0])]
  img2 = images[int(index[1])]
  if(Python == True):
    if(command == "PSNR-R"):
      PSNR = py_functions.py_r_psnr(img1, img2)
      print("Red PSNR:", PSNR)
    elif(command == "PSNR-G"):
      PSNR = py_functions.py_g_psnr(img1, img2)
      print("Green PSNR:", PSNR)
    elif(command == "PSNR-B"):
      PSNR = py_functions.py_b_psnr(img1, img2)
      print("Blue PSNR:", PSNR)
    elif(command == "PSNR"):
      PSNR = py_functions.py_total_psnr(img1, img2)
      print("PSNR of images:", PSNR)
  else:
    if(command == "PSNR-R"):
      PSNR = translation.call_c_r_psnr(img1, img2)
      print("Red PSNR:", PSNR)
    elif(command == "PSNR-G"):
      PSNR = translation.call_c_g_psnr(img1, img2)
      print("Green PSNR:", PSNR)
    elif(command == "PSNR-B"):
      PSNR = translation.call_c_b_psnr(img1, img2)
      print("Blue PSNR:", PSNR)
    elif(command == "PSNR"):
      PSNR = translation.call_c_total_psnr(img1, img2)
      print("PSNR of images:", PSNR)
  goto_begining()


def deal_help():
  print(" ")
  print("Commands:")
  print("load: Load a single image into the program for use")
  print("show: Display all images currently loaded")
  print("psnr-r: Calculate the PSNR between the red values for two colour images")
  print("psnr-g: Calculate the PSNR between the green values for two colour images")
  print("psnr-b: Calculate the PSNR between the blue values for two colour images")
  print("psnr: Calculate the PSNR between all values for two images")
  print("mode: Toggle mode between C and Python")
  print("help: Print out this command list")
  print("quit: Exit the PSNR Image Menu")
  goto_begining()


def deal_invalid():
  command = input("Invalid command.\n")
  command = command.upper().strip()
  command_match(command)


def command_match(command):
  if(command == "QUIT"):
    sys.exit()
  elif(command == "SHOW"):
    deal_show()
  elif(command == "MODE"):
    global Python
    Python = bool(1-Python)
    goto_begining()
  elif(command == "LOAD"):
    deal_load()
  elif(command[0:4] == "PSNR"):
    deal_PSNR(command)
  elif(command == "HELP"):
    deal_help()
  else:
    deal_invalid()


def goto_begining():
  print("\n--- PSNR Image Menu ---\n")
  mode = "C" if Python == False else "Python"
  print("Mode: "+mode)
  command = input("Type 'help' to see all commands\n").upper().strip()
  print()
  command_match(command)


print("Welcome to the PSNR image menu!")
goto_begining()
