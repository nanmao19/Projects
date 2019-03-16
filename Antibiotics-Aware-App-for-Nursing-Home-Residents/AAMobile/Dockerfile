# Add dockerfile script here to pull down the 
# image needed to build an apk file in Android Studio
FROM mingc/android-build-box:v1.4.0
MAINTAINER Wooyong Ee <wee3@gatech.edu>

COPY ./ /usr/src/app
WORKDIR /usr/src/app/AAMobile

# Run the Android exectuable build command `gradlew`.
# RUN cd /usr/src/app
RUN ./gradlew build
RUN cp app/build/outputs/apk/release/* /usr/src/app/AAWebServices/static/

# Install flask stuff.
WORKDIR /
RUN apt-get update
RUN apt-get install python-pip -y

WORKDIR /usr/src/app
RUN pip install --no-cache-dir -r ./AAWebServices/requirements.txt

ENV PYTHONPATH=.:/usr/src/app
EXPOSE 5000
CMD cd /usr/src/app/AAWebServices && python api.py