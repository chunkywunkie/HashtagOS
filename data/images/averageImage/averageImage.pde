/* 
Quick program to average images in src folder
*/

import java.util.List;

PImage dest;

void addImages(File folder, List<PImage> src)
{
    for (File entry : folder.listFiles()) {
      if (entry.isDirectory()) {
        addImages(entry, src);
      } else {
          try {
            String filename = folder.getPath() + "/" + entry.getName();
            PImage img = loadImage(filename);
            // only add valid images
            if (img.width != -1 && img.height != -1)
              src.add(img);
          } catch (Exception e) {
          }
      }
    }
}

void averageImages(List<PImage> src, PImage res)
{
  res.loadPixels();
  

  int dim = src.get(0).width*src.get(0).height;
  float accumColor[][] = new float[dim][3]; // store as floats so values don't max out to 255.
  
  // Accumulate source pixels to result
  for (PImage img : src) {
    img.loadPixels();
    for (int i = 0; i < img.height; i++) {
      for (int j= 0; j < img.width; j++) {
        int index = i + j*img.width;
        color c1 = img.pixels[index];
        
        accumColor[index][0] += red(c1);
        accumColor[index][1] += green(c1);
        accumColor[index][2] += blue(c1);
      }
    }
  }
  
  // Divide rgb values by total number of images
  for (int i = 0; i < res.height; i++) {
    for (int j= 0; j < res.width; j++) {
      int index = i + j*res.width;
      res.pixels[index] = color(accumColor[index][0]/src.size(), accumColor[index][1]/src.size(), accumColor[index][2]/src.size());
    }
  }
  res.updatePixels(); // finalize results
}

void setup()
{
  List<PImage> src = new ArrayList<PImage>();
    
  // hardcode, relative paths don't seem to work.
  String donut = "/Users/jchu/Documents/Academic/UCD/Spring2015/OS/Final Project/HashtagOS/data/images/donutday";
  String ucdavis = "/Users/jchu/Documents/Academic/UCD/Spring2015/OS/Final Project/HashtagOS/data/images/ucdavis";
  String playoffs = "/Users/jchu/Documents/Academic/UCD/Spring2015/OS/Final Project/HashtagOS/data/images/nbaplayoffs";
  String dog = "/Users/jchu/Documents/Academic/UCD/Spring2015/OS/Final Project/HashtagOS/data/images/dog";
  String starbucks = "/Users/jchu/Documents/Academic/UCD/Spring2015/OS/Final Project/HashtagOS/data/images/starbucks";
  String ucdavisPop = "/Users/jchu/Documents/Academic/UCD/Spring2015/OS/Final Project/HashtagOS/data/images/ucdavisPop"; // not conclusive
  String cat = "/Users/jchu/Documents/Academic/UCD/Spring2015/OS/Final Project/HashtagOS/data/images/cat";
  
  String infile = cat; // modify this.
  
  // place images in list of PImage objects
  File folder = new File(infile);
  addImages(folder, src);
  
  // presumably all images are same dimensions
  int imgWidth = src.get(0).width;
  int imgHeight = src.get(0).height;
  size(imgWidth, imgHeight);
  
  PImage res = createImage(imgWidth, imgHeight, RGB);
  dest = createImage(imgWidth, imgHeight, RGB);
  averageImages(src, res);
  dest.copy(res, 0, 0, imgWidth, imgHeight, 0, 0, imgWidth, imgHeight);
}


void draw()
{
  // show image
  image(dest, 0, 0);
}

void mouseClicked()
{
  save("result.jpg");
}
