# import cv2 as cv
# import os

# def test_image_loading(image_path):
#     # Überprüfe, ob die Datei existiert
#     if not os.path.exists(image_path):
#         print(f"Error: The file at {image_path} does not exist.")
#         return

#     # Versuche, das Bild zu laden
#     image = cv.imread(image_path)

#     if image is None:
#         print(f"Error: Failed to load image from {image_path}.")
#     else:
#         print(f"Success: Image loaded successfully from {image_path}.")
#         # Zeige das Bild in einem Fenster an (optional)
#         cv.imshow('Loaded Image', image)
#         cv.waitKey(0)  # Warte auf eine Tasteneingabe, bevor das Fenster geschlossen wird
#         cv.destroyAllWindows()

# if __name__ == "__main__":
#     # Pfad zu deinem Bild
#     image_path = "/Users/magnus/Desktop/fancybuddy/resources/images/fishing_template.png"
#     test_image_loading(image_path)
