from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from .models import FileUpload
from django.contrib import messages
# Create your views here.



################## Single Image Upload using File System Storage #######################################################
# def home(request):
#     if request.method == "POST":
#     # if the post request has a file under the input name 'document', then save the file.
#         request_file = request.FILES['document'] if 'document' in request.FILES else None
#         if request_file:
#                 # save attached file
    
#                 # create a new instance of FileSystemStorage
#                 fs = FileSystemStorage()
#                 file = fs.save(request_file.name, request_file)
#                 # the fileurl variable now contains the url to the file. This can be used to serve the file when needed.
#                 fileurl = fs.url(file)
 
#     return render(request, "tryupload/index.html")



############### Multiple Image Upload using File System Storage ##########################################################

def home(request):
    if request.method=="POST":
        # request_file = request.FILES['document'] if 'document' in request.FILES else None
        files = request.FILES.getlist('document')
        
        # print(files)
        
        a=[]
        if files:
            for file in files:
                fs = FileSystemStorage()
                filename = fs.save(file.name, file)
                file_url = fs.url(filename)
                a.append(file_url)
            
            fileurl=FileUpload(fileurl=a)
            messages.success(request,'images uploaded successfully.....')
            fileurl.save()
        
        return HttpResponseRedirect('/')
    else:
        images=FileUpload.objects.all()
        datadict={}
        for i in images:
            newid=i.id
            # file=i.fileurl
            newfile=((i.fileurl).lstrip('[')).rstrip(']')
            a=((newfile.replace("'","")).replace(" ","")).split(",")
            # print(a)
            for j in a:
                # print(j, i, "-------------")
                # if i.fileurl == "[]":
                #     i.delete()
                # else:
                    datadict[j[7:]]=newid
            #    print(datadict)
            #    print(f'value={j[7:]} and key={newid}')
            # print(images, 'qwertyuio')
            if images == None:
                print("see0000000000000000000")
            
        return render(request,'tryupload/index.html',{'images':images,'data':datadict})





########################## delete individual image #######################################################
def delete(request,pk,slug):
    if pk and slug:
        images=FileUpload.objects.get(pk=pk)
        url='/media/'+slug
        if images:
            newfile=((images.fileurl).lstrip('[')).rstrip(']')
            a=((newfile.replace("'","")).replace(" ","")).split(",")
            # print(type(a))
            print(a ,'BEFORE ###############################')
            b=list()
            for j in a:
                # print(j)
                # print(url)
                if j==url:

                    if len(a) == 1:
                        images.delete()
                    # if j == "[]":
                        # images.delete()
                    else:
                        a.remove(url)
                        images.fileurl=a
                        images.save()
                    
                    
                else:
                    # b.append(j)
                    # # print(b,'BBBBBBBBBBBBBBBBBBBBBBBBBBBBBB')
                    # images.fileurl=b
                    # images.save()
                    # if j == "[]":
                    #     images.delete()
                    pass
                
            # print(a,'After ################################')


        return HttpResponseRedirect('/')

########################### delete Complete Image Record ###########################
def deleteall(request,pk):
    if pk:
        images=FileUpload.objects.get(pk=pk)
        images.delete()
        return HttpResponseRedirect('/')



####################### Update Image ########################################
def update(request):
    if request.method=="POST":
        title='/media/'+request.POST.get('title')
        urlid=int(request.POST.get("id"))
        files = request.FILES.get('file')
        fs = FileSystemStorage()
        filename = fs.save(files.name, files)
        url = fs.url(filename)

        images=FileUpload.objects.get(pk=urlid)
        if images:
            newfile=((images.fileurl).lstrip('[')).rstrip(']')
            a=((newfile.replace("'","")).replace(" ","")).split(",")
            # print(a)
            for j in range(len(a)):
                # print(j)
                if a[j]==title:
                    a[j]=url
                    images.fileurl=a
                    images.save()
        
    return HttpResponseRedirect('/')
