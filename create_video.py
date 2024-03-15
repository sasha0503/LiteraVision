import cv2
import os


def create_video(image_paths, output_video_path, fps=0.5):
    # Determine the dimensions of the first image
    first_image = cv2.imread(image_paths[0])
    height, width, _ = first_image.shape

    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # You can use other codecs as well
    video_writer = cv2.VideoWriter(output_video_path, fourcc, fps, (width, height))

    # Iterate through each image and add it to the video
    for image_path in image_paths:
        frame = cv2.imread(image_path)
        video_writer.write(frame)

    # Release VideoWriter object
    video_writer.release()


# Example usage
if __name__ == "__main__":
    image_folders = [i for i in os.listdir() if i.startswith('output_folder')]
    output_video_path = "output_video.mp4"

    # Get all image paths in the folder
    image_paths = []
    for image_folder in image_folders:
        image_paths.extend([os.path.join(image_folder, image_name) for image_name in os.listdir(image_folder)])
    image_paths.sort()

    # Create the video with 2 frames per second
    create_video(image_paths, output_video_path, fps=1.5)
