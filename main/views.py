from django.shortcuts import render
from django.http import StreamingHttpResponse
from main.forms import HomeForm
from main.camera import VideoCamera, MobileCamera

# Create your views here.
# request -> response 
# view -> request handler / controller / action
# template -> presentation view 
# usage:
# pull date from db
# transform date
# send emails 
# frame = MainConfig.getFrame()
webCam = VideoCamera()
mobileCam = MobileCamera()

def main(request):
    return render(request, 'index.html')

def homepage_view(request):
    form = HomeForm()
    if request.method == 'POST':
        form = HomeForm(request.POST)
        if form.is_valid():
            alarmOn = form.cleaned_data.get("alarmActive")
            webCam.set_alarmOn(alarmOn)
            mobileCam.set_alarmOn(alarmOn)

    context = {
        'form': form,
    }
    return render(request, 'homepage.html', context)

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield ( b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

def webcam_feed(request):
    cam = webCam
    return StreamingHttpResponse(gen(cam), content_type="multipart/x-mixed-replace;boundary=frame")

def mobilecam_feed(request):
    cam = mobileCam
    return StreamingHttpResponse(gen(cam), content_type="multipart/x-mixed-replace;boundary=frame")