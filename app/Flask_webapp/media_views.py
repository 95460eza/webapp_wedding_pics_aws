
import logging
import os
import random
import base64
from io import BytesIO
import boto3
from flask import Flask, render_template, send_from_directory, send_file


# Flask Web App Setup
flask_web_app = Flask(__name__, static_folder="./Flask_webapp/static")
flask_web_app.config["DEBUG"] = True
#flask_web_app.config["DEBUG"] = False



# Specify your AWS credentials
aws_access_key_id = os.environ.get("AWS_ACCESS_KEY_ID")
aws_secret_access_key = os.environ.get("AWS_SECRET_ACCESS_KEY")
aws_session_token = os.environ.get("AWS_SESSION_TOKEN")

# Initialize the S3 client with your credentials
s3_client = boto3.client('s3',
                         aws_access_key_id=aws_access_key_id,
                         aws_secret_access_key=aws_secret_access_key,
                         aws_session_token=aws_session_token)

# Specify the bucket name
bucket_name = 'bucket-for-webapp-wedding-media--eun1-az1--x-s3'

image_list = []
image_data_list = []
image_stream_list = []


video_list = []
video_stream_list = []


prefix_image = "pictures_of_wedding/"
prefix_video = "videos_of_wedding/"


# Get List of objects in the bucket
media_object = s3_client.list_objects_v2(Bucket=bucket_name)

for obj in media_object['Contents']:

    # Create a "blob client" for EACH blob in the container
    #blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob.name)

    # Get the name of each media
    media_name = obj['Key']

    # Get the object corresponding to "a" picture
    media_as_picture_object = s3_client.get_object(Bucket=bucket_name, Key=media_name)


    if 'pictures_of_wedding' in media_name:

        # Create a list made of each PHOTO name
        image_list.append(media_name[len(prefix_image):])

        # Download the picture data as a stream of bytes
        picture_data = media_as_picture_object['Body'].read()

        # Convert the blob content to base64 to be used in HTML display code: render_template("show_image.html")
        base64_image = base64.b64encode(picture_data).decode('utf-8')
        image_data_list.append(base64_image)

        # Create a "blob client" for EACH blob in the container
        # blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob.name)
        # Download the blob content as a stream of bytes
        # blob_content = blob_client.download_blob().readall()
        # Create a BytesIO image stream object from the blob content to be USED in FLask module: flask.send_file(image_to_display)
        #image_stream = BytesIO(blob_content)
        #image_stream_list.append(image_stream)


        # # Convert Image.open() object to proper displaying format
        # def image_to_base64(image):
        #     # Convert PIL Image to base64 string
        #     image_buffer = BytesIO()
        #     image.save(image_buffer, format="PNG")
        #     image_data = base64.b64encode(image_buffer.getvalue()).decode("utf-8")
        #     return image_data


    else:

        # Create a list made of each VIDEO name
        video_list.append(media_name[len(prefix_video):])

        #video_stream_bytes = blob_client.download_blob().content_as_bytes()
        #video_stream = BytesIO(video_stream_bytes)
        #video_stream_list.append(video_stream)


# Shuffle IN PLACE the order of the pictures
combine_photos_name_and_data = list(zip(image_list, image_data_list))
random.shuffle(combine_photos_name_and_data)

image_list      = [tup[0] for tup in combine_photos_name_and_data]
image_data_list = [tup[1] for tup in combine_photos_name_and_data]


site_pages         = ["Photos of the Ceremony - Part I", "Photos of the Ceremony - Part II", "Photos of the Ceremony - Part III",
                      "Photos of the Ceremony - Part IV", "Films from the Wedding"]

number_photo_pages = len(site_pages)-1

# Integer part of division
integer_photos_per_page = len(image_list) / number_photo_pages



image_list1 = image_list[0:int(1*integer_photos_per_page)]
image_list2 = image_list[int(1*integer_photos_per_page):int(2*integer_photos_per_page)]
image_list3 = image_list[int(2*integer_photos_per_page):int(3*integer_photos_per_page)]
image_list4 = image_list[int(3*integer_photos_per_page):]

print()
print(len(image_list1), len(image_list2), len(image_list3), len(image_list4))
print()


image_data_list1 = image_data_list[0:int(1*integer_photos_per_page)]
image_data_list2 = image_data_list[int(integer_photos_per_page):int(2*integer_photos_per_page)]
image_data_list3 = image_data_list[int(2*integer_photos_per_page):int(3*integer_photos_per_page)]
image_data_list4 = image_data_list[int(3*integer_photos_per_page):]


# number_photos_displayed = 4
# image_list1 = image_list1[0:number_photos_displayed]
# print(image_list1)
# image_data_list1 = image_data_list1[0:number_photos_displayed]

# Create URL of Main Page:  http://127.0.0.1:5000 IF locally
@flask_web_app.route("/", methods=["GET"])
def home_page():
    list_of_names_for_main_webpage = site_pages
    return render_template('index.html', names=list_of_names_for_main_webpage)


@flask_web_app.route("/Photos of the Ceremony - Part I", methods=["GET"])
def show_all_photos1():
    zipped_lists1 = zip(image_list1, image_data_list1)
    return render_template("show_image.html", list_of_pics=zipped_lists1)

@flask_web_app.route("/Photos of the Ceremony - Part II", methods=["GET"])
def show_all_photos2():
    zipped_lists2 = zip(image_list2, image_data_list2)
    return render_template("show_image.html", list_of_pics=zipped_lists2)

@flask_web_app.route("/Photos of the Ceremony - Part III", methods=["GET"])
def show_all_photos3():
    zipped_lists3 = zip(image_list3, image_data_list3)
    return render_template("show_image.html", list_of_pics=zipped_lists3)

@flask_web_app.route("/Photos of the Ceremony - Part IV", methods=["GET"])
def show_all_photos4():
    zipped_lists4 = zip(image_list4, image_data_list4)
    return render_template("show_image.html", list_of_pics=zipped_lists4)


@flask_web_app.route("/Films from the Wedding", methods=["GET"])
def show_all_videos():
    # print(video_list)
    return render_template("show_video.html", list_of_videos=video_list)




# A Route ENDPOINT is a FIXED name: Here "/images".
# Then "/<path:filename>" means that if a REQUEST is made to any URL that has something EXTRA AFTER "/images/", THAT extra will be PUT into the variable "filename" and passed as
# the argument of the function.
# The "path" CONVERTER asks to capture "/". Ex: if a request is sent to '/images/some_folder/some_image.jpg', Flask will pass the part 'some_folder/some_image.jpg' as the value
# of for filename in the function. In general, an HTML file will send those requests with the "EXTRA" mentioned above
@flask_web_app.route('/images/<path:filename>')
def serve_image(filename):

    # Get the index of the filename in the image_list
    #image_index = image_list.index(filename)

    # Get the BytesIO image stream object CORRESPONDING to that filename
    #image_stream = image_stream_list[image_index]

    # RE-SAVE the image_stream element b/c gets closed EACH TIME USED!!!!
    #image_stream_list[image_index] = image_stream
    # print(image_stream)


    # Get the object corresponding to the image
    media_as_pict_object = s3_client.get_object(Bucket=bucket_name, Key=prefix_image + filename)
    # Download the picture data as a stream of bytes
    pic_data = media_as_pict_object['Body'].read()
    # Create a BytesIO image stream object from the blob content to be used FLask module: flask.send_file(image_to_display)
    image_stream = BytesIO(pic_data)

    # Display the image file with the appropriate MIME type
    # return send_from_directory(image_folder, filename)
    return send_file(image_stream, mimetype='image/jpeg')


@flask_web_app.route('/videos/<path:video_path>')
def serve_video(video_path):

    # Concatenate names of folder with videos and name specific video received via variable "video_path" when link clicked at route above
    # full_video_path = video_folder2 + '/' + video_path
    # print(full_video_path)

    # Get the index of the video name in the video_list
    #video_index = video_list.index(video_path)

    # Get the streamable data CORRESPONDING to that video
    #video_stream = video_stream_list[video_index]

    # RE-SAVE the video_stream element b/c gets closed EACH TIME USED!!!!
    #video_stream_list[video_index] = video_stream

    # Get the object corresponding to the image
    media_as_video_object = s3_client.get_object(Bucket=bucket_name, Key=prefix_video + video_path)
    # Download the picture data as a stream of bytes
    video_stream_bytes = media_as_video_object['Body'].read()

    #blob_client = blob_service_client.get_blob_client(container=container_name, blob=prefix_video + video_path)
    # Download the video content as a stream of bytes
    #video_stream_bytes = blob_client.download_blob().content_as_bytes()

    # Wrap the bytes into a BytesIO object
    video_stream = BytesIO(video_stream_bytes)

    return send_file(video_stream, mimetype='video/mp4')



# Always LAST statements of the file
# Zappa requires the handler function to be named `lambda_handler`
def lambda_handler(event, context):
    
    try:

        logging.info("Lambda Event: %s", event)
        response = flask_web_app(event, context)
        return response

    except Exception as e:

        # Log the exception
        logging.info("Lambda Event: %s", event)
        logging.error("An error HAS occurred: %s", event)
        logging.error("An error HAS occurred: %s", str(e))
        