from logging import getLogger
import os

from django.db.models.functions import Lower
from django.template.loader import render_to_string

from .models import Category, Country, Solution, AllSites, UserRecentSite


logger = getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

#nginx will be used directly to serve this big page
#something like this
# location /QuickLink {
#     location /QuickLink/static {
#         alias /opt/temp/django/quicklink/stat;
#     }
#     location /QuickLink/home/allsite {
#         alias /opt/temp/django/quicklink/templates/generic/include/table_s.html;
#     }
#    include uwsgi_params;
#    uwsgi_pass unix:/run/uwsgi/quicklink.sock;
#    uwsgi_param Host $host;
#    uwsgi_param X-Real-IP $remote_addr;
#    uwsgi_param X-Forwarded-For $proxy_add_x_forwarded_for;
#    uwsgi_param X-Forwarded-Proto $http_x_forwarded_proto;
# }
def create_table_include():
    logger.debug('create_table_include')
    context = {}
    
    context['all_sites'] = AllSites.objects.all().order_by(Lower('name')) 
    
    file = '{}/templates/generic/include/table_s.html'.format(BASE_DIR)
    logger.debug('file to write : {}'.format(file))
    q = render_to_string ('generic/include/table.html', context)
    with open(file, 'w') as f:
        f.write(q)
    logger.info('table_s.html generated successfully')
    

def create_onnew_include():
    logger.debug('inside create_category_include')
    context = {}
    
    context['all_country'] = Country.objects.all().order_by('listorder', Lower('country')) 
    context['all_solution'] = Solution.objects.all().order_by('listorder', Lower('solution'))
    context['all_category'] = Category.objects.all().order_by('listorder', Lower('category'))
    
    file = '{}/templates/generic/include/country_radio_s.html'.format(BASE_DIR)
    logger.debug('file to write : {}'.format(file))
    q = render_to_string ('generic/helper/country_radio.html', context)
    with open(file, 'w') as f:
        f.write(q)
    logger.info('country_radio_s.html generated successfully')
    
    file = '{}/templates/generic/include/nav_select_s.html'.format(BASE_DIR)
    logger.debug('file to write : {}'.format(file))
    q = render_to_string ('generic/helper/nav_select.html', context)
    with open(file, 'w') as f:
        f.write(q)
    logger.info('nav_select_s.html generated successfully')
    
def batch_upload_processing(infile, ipaddress, update_existing):
    batch_output = []
    for line in infile:
        try:
            rowline = line.decode('utf-8')
            rowvalue = rowline.split('~')
            #check if row exist
            if AllSites.objects.filter(name=rowvalue[0]).exists():
                if update_existing:
                    batch_output.append('{} already exists, update flag is on, site will be updated'.format(rowvalue[0]))
                    allsite = AllSites.objects.get(name=rowvalue[0])
                else:
                    batch_output.append('{} already exist, update flag is off, site will not be updated'.format(rowvalue[0]))
                    continue
            else:
                allsite = AllSites()
                
            allsite.name = rowvalue[0]
            logger.debug('row1 {}'.format(rowvalue[1]))
            allsite.category = Category.objects.get(pk=rowvalue[1].strip())
            allsite.country = Country.objects.get(pk=rowvalue[2])
            allsite.solution = Solution.objects.get(pk=rowvalue[3])
            if rowvalue[4].strip():
                allsite.testurl_direct = rowvalue[4]
            if rowvalue[5].strip():    
                allsite.testurl_indirect = rowvalue[5]
            if rowvalue[6].strip():
                allsite.systurl_direct = rowvalue[6]
            if rowvalue[7].strip():
                allsite.systurl_indirect = rowvalue[7]
            if rowvalue[8].strip():
                allsite.produrl_direct = rowvalue[8]
            if rowvalue[9].strip():
                allsite.produrl_indirect = rowvalue[9]
            
            allsite.last_modified_by = ipaddress
            allsite.save()
            batch_output.append('success : ' + rowvalue[0] + ' processed successfully')
        except Exception as e:
            logger.error('exception occur : {}'.format(str(e)), exc_info=True)
            batch_output.append('failure : ' + str(e) + ' exception occur while processing ' + rowvalue[0])
            
    return batch_output


def update_recent_io(ipaddress, siteid):
    response = {}
    success_message = ''
    try:
        if UserRecentSite.objects.filter(userid=ipaddress, site_id=siteid).exists():
            logger.debug('site exist, updating timestamp')
            instance = UserRecentSite.objects.get(userid=ipaddress, site_id=siteid)
            instance.save() #this will update timestamp
            success_message = success_message + 'site updated successfully'
            response['rt'] = success_message
        else:
            logger.debug('site does not exist, inserting new row')
            allsiteid = AllSites.objects.get(pk=siteid)
            recentrow = UserRecentSite(userid=ipaddress, site_id=allsiteid)
            recentrow.save()
            success_message = success_message + 'site inserted successfully'
            response['rt'] = success_message
        #delete excess rows
        queryres = UserRecentSite.objects.filter(userid=ipaddress).order_by('-updated_at')[20:]
        for queryrow in queryres:
            queryrow.delete()
        success_message = success_message + ' ; extra rows deleted successfully'
        response['rc'] = '00'
        response['rt'] = success_message    
    except Exception as e:
        response['rc'] = '99'
        response['rt'] = 'error updating recent site {}'.format(str(e))
        logger.error('exception occur {}'.format(str(e)), exc_info=True)
        
    return response

def get_ip_address(request):
    if 'X-Real-IP' in request.META:
        ipaddress = request.META['X-Real-IP']
    else:
        ipaddress = request.META['REMOTE_ADDR']
    return ipaddress
    

    
    

    
    