#!/usr/bin/env bash                                                                                                                                                     
# Sets up a web server for deployment of web_static. 

sudo apt-get update
sudo apt-get install -y nginx

mkdir -p /data/web_static/releases/test/
mkdir -p /data/web_static/shared/
echo "Hello World!" > /data/web_static/releases/test/index.html
ln -sf /data/web_static/releases/test/ /data/web_static/current

chown -R ubuntu /data/
chgrp -R ubuntu /data/

printf %s "server {                                                                                                                                                     
     listen      80 default_server;                                                                                                                                     
     listen      [::]:80 default_server;                                                                                                                                
     add_header X-Served-By $HOSTNAME;                                                                                                                                  
     root        /etc/nginx/html;                                                                                                                                       
     index       index.html index.htm;                                                                                                                                  
                                                                                                                                                                        
     location /redirect_me {                                                                                                                                            
        return 301 https://scott-techstar.github.io/;                                                                                                                   
    }                                                                                                                                                                   
                                                                                                                                                                        
    error_page 404 /404.html;                                                                                                                                           
    location /404 {                                                                                                                                                     
      root /etc/nginx/html;                                                                                                                                             
      internal;                                                                                                                                                         
    }                                                                                                                                                                   
}                                                                                                                                                                       
" > /etc/nginx/sites-available/default

service nginx restart
