
	var map;
	var infowindow;
    // 移动到相应教学楼
	function MoveToBuilding(e){
		x = e.cells["lat"].innerHTML;
		y = e.cells["lng"].innerHTML;
		//name = e.cells['buildingname'].innerHTML.toString();
		var location = new google.maps.LatLng(parseFloat(x),parseFloat(y));
		map.setCenter(location);
		map.setZoom(18);
	}
  	// 把教学楼标注到地图上~
  	function AddMarkers()
  	{
  		var rows = document.getElementsByTagName("tr");
  		// 从第二行开始
  		for(i=1; i< rows.length; i++){
  			name = rows[i].cells['buildingname'].innerHTML.toString();
  			lat = rows[i].cells["lat"].innerHTML.toString();
  			lng = rows[i].cells["lng"].innerHTML.toString();
	  		var location = new google.maps.LatLng(parseFloat(lat),parseFloat(lng));
	  		var marker = new google.maps.Marker({
				  position: location,
				  map: map,
				  title: name
			});
  		};
  	}
  	// 隐藏 坐标列
  	function HideLatLng(){
  		rows = document.getElementsByTagName("tr");
  		for(i=0; i < rows.length; i++){
  			rows[i].cells["lat"].style.display = "none";
  			rows[i].cells["lng"].style.display = "none";
  		}
  	}  
    // 初始化地图...
    function initialize(){
   	 	HideLatLng();
   	 	//alert('1');
        var Whu = new google.maps.LatLng(30.54003554209287,114.36588406562805);
        var myOptions = {
            zoom: 16,
            center: Whu,
            mapTypeId: google.maps.MapTypeId.SATELLITE
        };
        map = new google.maps.Map(document.getElementById("map_canvas"), myOptions);
        // 然后在页面上添加marker
        AddMarkers();
    }
  	// 
  	google.maps.event.addDomListener(window, 'load', initialize);
