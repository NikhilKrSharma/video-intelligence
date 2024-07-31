from TrackerModules.SortDetection import detectObject

def main():
    # Clear the console (if running interactively)
    import os
    os.system('clear')  # On Windows, use os.system('cls')

    # Get user input for source and options
    try:
        source = int(input("Camera (1), Preloaded Video (2): "))
        if source not in [1, 2]:
            print("Invalid option for source. Please enter 1 or 2.")
            return

        videoPath = None
        if source == 2:
            videoPath = f"{input('Enter Video File Name: ').strip()}.mp4"

        viewVideo = input("View Processing in Real Time (Y/N): ").upper() == 'Y'
        saveVideo = input("Save the Video (Y/N): ").upper() == 'Y'

        # Call the detection function with the provided inputs
        detectObject(source, videoPath, saveVideo, viewVideo)

    except ValueError:
        print("Invalid input. Please enter numeric values where required.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()