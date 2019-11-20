(function() {
  var zoom = 20;
  var canvas = document.getElementById('Canvas'),
      context = canvas.getContext('2d');
  var bplus = document.getElementById("buttonplus");
  var bminus = document.getElementById("buttonminus");
  //suppose we have an array of absolute point coordenates
  //suppoising we receive in this format [X1,y1,X2,y2.......]
  var numpoints = 5;
  var pointsXY = [1,1,5,5,1,4,5,8,10,10];
  var pointsWH = new Array(numpoints*2);
  var center = [5,5];
  var mouseprev = [-1,-1];
  // Event handler to resize the canvas when the document view is changed


  window.addEventListener('resize', resizeCanvas, false);
  bplus.addEventListener("click",zoomplus);
  bminus.addEventListener("click",zoomminus);

  canvas.addEventListener('mousedown',handleclick, false);
  canvas.addEventListener("mouseup",handlerelease, false);

  function checkifvisible(display_x,display_y){
    if(display_x < 0 || display_x >canvas.width )
        return 0;
    if(display_y < 0 || display_y >canvas.height )
        return 0;
    return 1;
  }
  function coorconverter(X,Y){
      //basically the center has to be mapped on the center
      //and the zoom corresponds to the inverse off max distance shown
      display_x = (zoom)*(X-center[0])+ canvas.width/2;
      display_y = (zoom)*(Y-center[1])+ canvas.height/2;
      vis = checkifvisible(display_x,display_y);
      if(vis==0){
        display_x = -1;
        display_y = -1;
      }
      return [display_x,display_y]
  }

  function inversecoord(display_x,display_y){
    X = (display_x-canvas.width/2)/zoom+center[0];
    Y = (display_y-canvas.height/2)/zoom+center[1];
    return [X,Y]
  }

  function handleclick(event){
    mouseprev[0] = event.pageX;
    mouseprev[1] = event.pageY;
    canvas.addEventListener("mousemove",handlemove, false);
  }
  function abs(a){
    if (a>0)
      return a;
      return -a;
  }
  function handlemove(event){
    dispx = event.pageX;
    dispy = event.pageY;
    if(abs(dispx-mouseprev[0])+abs(dispy-mouseprev[1])>10){
      [cx,cy] = inversecoord(dispx,dispy);
      [px,py] = inversecoord(mouseprev[0],mouseprev[1]);
      center[0] = center[0] + (px-cx);
      center[1] = center[1] + (py-cy);
      drawStuff();
      mouseprev[0] = event.pageX;
      mouseprev[1] = event.pageY;
    }
  }
  function handlerelease(event){
      canvas.removeEventListener("mousemove",handlemove, false);

  }

  function vectorconverter(){
    for (i=0;i<numpoints*2;i = i+2){
      [dispx,dispy] = coorconverter(pointsXY[i],pointsXY[i+1]);
      pointsWH[i]  = dispx;
      pointsWH[i+1]= dispy;
    }
  }

  function zoomplus(){
    zoom =zoom + 2;
    drawStuff();
  }

  function zoomminus(){
    zoom =zoom - 2;
    if(zoom<=0){
      zoom = 1;
    }

    drawStuff();
  }

  function resizeCanvas() {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
    // Redraw everything after resizing the window

    drawStuff();
  }

  resizeCanvas();

  function drawStuff() {
    vectorconverter()
    // Do drawing here
    context.clearRect(0, 0, canvas.width, canvas.height);
    context.strokeRect(0,0,canvas.width ,canvas.height);
    for (i=0;i<2*numpoints;i+=2){
       if(pointsWH[i] != -1 && pointsWH[i+1] != -1 )
          context.strokeRect(pointsWH[i],pointsWH[i+1],8,8);
    }

  }
})();
