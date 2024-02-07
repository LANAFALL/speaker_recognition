from pydub import AudioSegment
from pydub.silence import detect_silence
import os

def convert_to_wav(input_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    supported_extensions = ['.m4a', '.mp3', '.aac', '.wav']

    for filename in os.listdir(input_folder):
        if filename.lower().endswith(tuple(supported_extensions)):
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, os.path.splitext(filename)[0] + '.wav')

            audio = AudioSegment.from_file(input_path)

            audio.export(output_path, format='wav')

            print(f"Converted to WAV: {filename}")

def remove_silence(input_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    total_time_before_silence = 0
    total_time_after_silence = 0

    for filename in os.listdir(input_folder):
        if filename.lower().endswith('.wav'):
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, filename)

            # Load the audio file
            audio = AudioSegment.from_file(input_path)

            # Calculate total time before silence removal
            total_time_before_silence += len(audio)

            # Detect silence and concatenate non-silent segments
            non_silent_segments = detect_silence(audio, silence_thresh=-30)

            # Ensure all non-silent segments have the same sample width and frame rate
            sample_width = audio.sample_width
            frame_rate = audio.frame_rate

            result_audio = AudioSegment.silent()
            for start, end in non_silent_segments:
                # Load each non-silent segment
                segment = audio[start:end]

                # Ensure the segment has the same sample width and frame rate
                if segment.sample_width != sample_width or segment.frame_rate != frame_rate:
                    segment = segment.set_frame_rate(frame_rate).set_sample_width(sample_width)

                result_audio += segment

            # Export the result to the output folder
            result_audio.export(output_path, format="wav")

            # Calculate total time after silence removal
            total_time_after_silence += len(result_audio)

    print(f"Total time before silence removal: {total_time_before_silence / 1000} seconds")
    print(f"Total time after silence removal: {total_time_after_silence / 1000} seconds")

def split_audio(input_folder, output_folder, segment_length=3000):
    # Ensure output folder exists
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    total_time = 0
    total_files = 0

    # Iterate through each file in the input folder
    for filename in os.listdir(input_folder):
        if filename.endswith(".wav"):
            file_path = os.path.join(input_folder, filename)

            # Load audio file
            audio = AudioSegment.from_file(file_path)

            # Calculate the number of segments
            num_segments = len(audio) // segment_length

            # Split audio into segments
            for i in range(num_segments):
                start_time = i * segment_length
                end_time = start_time + segment_length

                segment = audio[start_time:end_time]

                # Save the segment to the output folder
                output_filename = f"{filename.split('.')[0]}_{i + 1}.wav"
                output_path = os.path.join(output_folder, output_filename)
                segment.export(output_path, format="wav")

                total_time += len(segment)
                total_files += 1

    print(f"Total files extracted: {total_files}")
    print(f"Total time of all files: {total_time / 1000} seconds")

if __name__ == "__main__":
    person = "Krankrai"
    input_folder = f"C:\\Users\\ASUS\\Desktop\\spreaker_recog\\2_original_voice\\{person}"
    output_folder_wav_temp = f"C:\\Users\\ASUS\\Desktop\\spreaker_recog\\wav_temp\\{person}"
    output_folder_silent_temp = f"C:\\Users\\ASUS\\Desktop\\spreaker_recog\\silent_temp\\{person}"
    output_folder_final = f"C:\\Users\\ASUS\\Desktop\\spreaker_recog\\16000_pcm_speeches\\audio\\{person}"

    # Convert to WAV first
    # convert_to_wav(input_folder, output_folder_wav_temp)

    # Remove silence from WAV files
    # remove_silence(output_folder_wav_temp, output_folder_silent_temp)

    # Split the resulting audio into segments
    split_audio(output_folder_silent_temp, output_folder_final)
