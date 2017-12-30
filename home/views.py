import logging

from django.db.models.functions.base import Lower
from django.http.response import Http404  # @UnusedImport
from django.http.response import JsonResponse
from django.shortcuts import render, redirect

from . import forms
from . import models
from . import utils


logger = logging.getLogger(__name__)

def home(request):
    context = {}
    return render(request, 'home/index.html', context)

# Create your views here.
def allsite(request):
    # this big static table_s.html page is generated only when any site is modified
    # we will use nginx to server this big page, this will save big query fetch of all site and rendering every time
    return render(request, 'generic/include/table_s.html')
    
def recentsite(request):
    rowcount = request.GET.get('rowcount', None)
    if rowcount:
        try:
            introwcount = int(rowcount)
            logger.debug('recent site will show {} rows'.format(introwcount))
        except Exception as e:
            logger.error('exception occur {}'.format(str(e)), exc_info=True)
    else:
        rowcount = 15
        logger.info('recent site count is not in request, default 15 will be used')
        
    context = {}
    ipadd = utils.get_ip_address(request)
    tablerowsid = models.UserRecentSite.objects.filter(userid=ipadd).order_by('-updated_at')[:introwcount]
    all_sites = []
    for rowid in tablerowsid:
        siteid = rowid.site_id.id
        all_sites.append(models.AllSites.objects.get(pk=siteid))
    context['all_sites'] = all_sites
    return render(request, 'generic/include/table.html', context)

def addsite(request):
    if request.method == 'POST':
        form = forms.AddSite(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.last_modified_by = utils.get_ip_address(request)
            logger.info('adding new site {} by {}'.format(obj, request.user.username))
            try:
                obj.save()
                return redirect('success')
            except Exception as e:
                logger.error('exception occur {}'.format(str(e)), exc_info=True)
                return redirect('failure')
        else:
            context = {}
            context['form'] = form;
            context['hide_navbar_content'] = True  # hide nav content
            return render(request, 'home/addsite.html', context)
    else:
        form = forms.AddSite()
        context = {}
        context['form'] = form;
        context['hide_navbar_content'] = True  # hide nav content
        return render(request, 'home/addsite.html', context)


def modtable(request):
    context = {}
    context['all_sites'] = models.AllSites.objects.all().order_by(Lower('name'))
    context['hide_recent_button'] = True
    return render(request, 'home/modtable.html', context) 

def editsite(request):
    if request.method == 'POST':
        rowid = request.session.get('rowid')
        logger.debug('rowid in editsite post {}'.format(rowid))
        row = models.AllSites.objects.get(pk=rowid)
        form = forms.AddSite(request.POST, instance=row)
                
        if form.is_valid():
            obj = form.save(commit=False)
            obj.last_modified_by = utils.get_ip_address(request)
            logger.info('edit site  {} by {}'.format(obj, utils.get_ip_address(request)))
            try:
                obj.save()
                return redirect('success')
            except Exception as e:
                logger.error('exception occur {}'.format(str(e)), exc_info=True)
                return redirect('failure')
        else:
            context = {}
            context['hide_navbar_content'] = True  # hide nav content
            context['form'] = form;
            return render(request, 'home/editsite.html', context)
    else:
        try:
            rowid = request.GET['rowid']
            request.session['rowid'] = rowid
            logger.debug('get method, id requested {}'.format(rowid))
            row = models.AllSites.objects.get(pk=rowid)
            form = forms.AddSite(instance=row)
            context = {}
            context['hide_navbar_content'] = True  # hide nav content
            context['form'] = form;
            return render(request, 'home/editsite.html', context)
        except:
            logger.info('{} try to access editsite indirectly'.format(request.user.username))
            raise Http404
        
def deletesite(request):
    if request.method == 'POST':
        rowid = request.session.get('rowid')
        logger.debug('rowid in deletesite post {}'.format(rowid))
        del request.session['rowid']
        try:
            row = models.AllSites.objects.get(pk=rowid)
            row.delete()
            return redirect('success')
        except Exception as e:
            logger.info('exception occur {}'.format(str(e)), exc_info=True)
            return redirect('failure')
    else:
        try:
            rowid = request.GET['rowid']
            request.session['rowid'] = rowid
            logger.debug('get method of deletesite, id requested {}'.format(rowid))
            row = models.AllSites.objects.get(pk=rowid)
            form = forms.AddSite(instance=row)
            context = {}
            context['hide_navbar_content'] = True  # hide nav content
            context['form'] = form;
            return render(request, 'home/delsite.html', context)
        except:
            logger.info('{} try to access delsite indirectly'.format(request.user.username))
            raise Http404 
        
def batchupload(request):
    if request.method == 'POST':
        form = forms.BatchUploadForm(request.POST, request.FILES)
        if form.is_valid():
            logger.debug('ost data {}'.format(request.POST))
            infile = request.FILES['file']
            update_existing = request.POST.get('update_existing')
            logger.debug('update existing site {}'.format(update_existing))
            ipaddress = utils.get_ip_address(request)
            logger.debug('ipaddress {}'.format(ipaddress))
            batch_output = utils.batch_upload_processing(infile, ipaddress, update_existing)
            context = {}
            context['batch_output'] = batch_output
            context['hide_navbar_content'] = True  # hide nav content
            context['show_result'] = True
            return render(request, 'home/upload.html', context)    
        else:
            context = {}
            context['hide_navbar_content'] = True  # hide nav content
            context['show_upload'] = True
            context['form'] = form;
            return render(request, 'home/upload.html', context)
    else:
        form = forms.BatchUploadForm()
        context = {}
        context['hide_navbar_content'] = True  # hide nav content
        context['form'] = form
        context['show_upload'] = True
        return render(request, 'home/upload.html', context)
    
def refresh(request):
    try:
        data = {'rc':'00', 'rt':'all_ok'}
        utils.create_onnew_include()
        utils.create_table_include()
    except Exception as e:
        data = {'rc':'99', 'rt':str(e)}
    return JsonResponse(data) 

def successmsg(request):
    context = {}
    context['hide_navbar_content'] = True  # hide nav content
    context['msg'] = "Congrats!!! Operation Successful!!" 
    context['url'] = "/QuickLink/home/"
    context['bt'] = "Take me to homepage"
    return render(request, 'common/success.html', context)

def failuremsg(request):
    context = {}
    context['hide_navbar_content'] = True  # hide nav content
    context['msg'] = "Oops!!! Operation failed!!" 
    context['url'] = "/QuickLink/home/"
    context['bt'] = "Take me to homepage"
    return render(request, 'common/failure.html', context)

def updaterecent(request):
    if request.method == 'GET':
        try:
            siteid = request.GET['siteid']
            ipaddress = utils.get_ip_address(request)    
            logger.debug('get method, id requested {}, ip {}'.format(siteid, ipaddress))
            response = utils.update_recent_io(ipaddress, siteid) 
            return JsonResponse(response)     
        except Exception as e:
            logger.error('exception occur : {}'.format(str(e)), exc_info=True)
            return JsonResponse({'rc':'99', 'rt':str(e)})
    else:
        raise Http404
    
def helppage(request):
    context = {}
    context['hide_navbar_content'] = True  # hide nav content
    return render(request, 'home/help.html', context)