# Image Gallery

This project is built for `Winter 2022 - Shopify
Developer Intern Challenge Question`.  


**Almost done!**  
**I'll update a `docker-compose` file to let you deploy the whole system easily.`(Before 23:59 PM Sep 24 2021, Ottawa time)`** 

## Run and Test (developing mode rather than production)
``` bash
docker run -it -p 5000:5000 --rm triose/image_gallary:v1
```


`TODO`  
- [x] Frontend pages design and implementation
- [x] File upload, save, display
- [x] Build docker image for tensorflow model server serving a SSD300 model
- [x] Object detection model inference functions
- [x] Used HDF5 to store images
- [x] image feature extraction process when images are uploaded
- [x] NLP word2vec to implement image text searching 
- [x] Examples in README.md
- [ ] Multiple threads in production environment
- [ ] Code comments and beautify
- [ ] Docker image for deployment and document
- [ ] Optimization


Reference:
> Web pages templates: METRONIC https://keenthemes.com/metronic/  
> Image player in the dashboard: https://www.html5tricks.com/jquery-accordion-auto-image-player.html  
> SSD Kears: https://github.com/pierluigiferrari/ssd_keras  


## Examples of image searching
![](./example_imgs/search_term_cat.png)  
![](./example_imgs/search_term_car.png)  
![](./example_imgs/search_by_my_photo.png)  
![](./example_imgs/search_by_a_train_photo.png)  
![](./example_imgs/search_by_flowers.png)  
