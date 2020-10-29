function createGeodesicPolygon(origin, radius, sides, rotation, projection) {
    var latlon = origin; //leaflet equivalent
    var angle;
    var new_lonlat, geom_point;
    var points = [];
    for (var i = 0; i < sides; i++) {
      angle = (i * 360 / sides) + rotation;
      new_lonlat = destinationVincenty(latlon, angle, radius);
      geom_point = L.latLng(new_lonlat.lng, new_lonlat.lat);

      points.push(geom_point);
    }
    return points;
}

L.Util.VincentyConstants = {
    a: 6378137,
    b: 6356752.3142,
    f: 1/298.257223563
};

function destinationVincenty(lonlat, brng, dist) { //rewritten to work with leaflet
    var u = L.Util;
    var ct = u.VincentyConstants;
    var a = ct.a, b = ct.b, f = ct.f;
    var lon1 = lonlat.lng;
    var lat1 = lonlat.lat;
    var s = dist;
    var pi = Math.PI;
    var alpha1 = brng * pi/180 ; //converts brng degrees to radius
    var sinAlpha1 = Math.sin(alpha1);
    var cosAlpha1 = Math.cos(alpha1);
    var tanU1 = (1-f) * Math.tan( lat1 * pi/180 /* converts lat1 degrees to radius */ );
    var cosU1 = 1 / Math.sqrt((1 + tanU1*tanU1)), sinU1 = tanU1*cosU1;
    var sigma1 = Math.atan2(tanU1, cosAlpha1);
    var sinAlpha = cosU1 * sinAlpha1;
    var cosSqAlpha = 1 - sinAlpha*sinAlpha;
    var uSq = cosSqAlpha * (a*a - b*b) / (b*b);
    var A = 1 + uSq/16384*(4096+uSq*(-768+uSq*(320-175*uSq)));
    var B = uSq/1024 * (256+uSq*(-128+uSq*(74-47*uSq)));
    var sigma = s / (b*A), sigmaP = 2*Math.PI;
    while (Math.abs(sigma-sigmaP) > 1e-12) {
        var cos2SigmaM = Math.cos(2*sigma1 + sigma);
        var sinSigma = Math.sin(sigma);
        var cosSigma = Math.cos(sigma);
        var deltaSigma = B*sinSigma*(cos2SigmaM+B/4*(cosSigma*(-1+2*cos2SigmaM*cos2SigmaM)-
            B/6*cos2SigmaM*(-3+4*sinSigma*sinSigma)*(-3+4*cos2SigmaM*cos2SigmaM)));
        sigmaP = sigma;
        sigma = s / (b*A) + deltaSigma;
    }
    var tmp = sinU1*sinSigma - cosU1*cosSigma*cosAlpha1;
    var lat2 = Math.atan2(sinU1*cosSigma + cosU1*sinSigma*cosAlpha1,
        (1-f)*Math.sqrt(sinAlpha*sinAlpha + tmp*tmp));
    var lambda = Math.atan2(sinSigma*sinAlpha1, cosU1*cosSigma - sinU1*sinSigma*cosAlpha1);
    var C = f/16*cosSqAlpha*(4+f*(4-3*cosSqAlpha));
    var lam = lambda - (1-C) * f * sinAlpha *
        (sigma + C*sinSigma*(cos2SigmaM+C*cosSigma*(-1+2*cos2SigmaM*cos2SigmaM)));
    // var revAz = Math.atan2(sinAlpha, -tmp);  // final bearing
    var lamFunc = lon1 + (lam * 180/pi); //converts lam radius to degrees
    var lat2a = lat2 * 180/pi; //converts lat2a radius to degrees

    return L.latLng(lamFunc, lat2a);

}

SinglePolygonFieldStore = L.FieldStore.extend({

    _layerToJson: function (layer) {
      const json = layer.toGeoJSON();
      if (layer instanceof L.Circle) {
        json.properties.radius = layer.getRadius();
      }
      return json;
    },

    load: function () {
        return this.formfield.value || '';
    },

    save: function (layer) {
        this.formfield.value = JSON.stringify(this._layerToJson(layer));
    },

    clear: function() {
        this.formfield.value = '';
    },

    getOptions: function() {
        return $(this.formfield).data();
    }
});

SinglePolygonGeometryField = L.GeometryField.extend({

    options: {
        field_store_class: SinglePolygonFieldStore,
    },

    _controlDrawOptions: function () {
        return {
            edit: {
                featureGroup: this.drawnItems
            },
            draw: {
                polyline: this.options.is_linestring,
                polygon: this.options.is_polygon,
                circle: true, // Turns off this drawing tool
                rectangle: this.options.is_polygon,
                marker: this.options.is_point,
            }
        };
    },

    addTo: function (map) {

        function fixLayerNativeZoom() {
            let mapLayer = Object.values(map._layers).find(layer => layer._url !== undefined);
            if (!mapLayer.options.fixed) {
                mapLayer.options.maxNativeZoom = mapLayer.options.maxZoom;
                mapLayer.options.maxZoom = 22;
            }
            mapLayer.options.fixed = true;
        }

        fixLayerNativeZoom();
        map.on('baselayerchange', fixLayerNativeZoom);
        // setTimeout(function() {
        //     fixLayerNativeZoom();
        //     map.invalidateSize();
        // }, 4000);

        L.Draw.Circle.prototype._drawShape = function (latlng) {
          if (!this._shape) {
            this._shape = new L.GreatCircle(this._startLatLng, this._startLatLng.distanceTo(latlng), this.options.shapeOptions);
            this._map.addLayer(this._shape);
          } else {
            this._shape.setRadius(this._startLatLng.distanceTo(latlng));
          }
        };

        this._map = map;
        let store_opts = L.Util.extend(this.options, {defaults: map.defaults});
        this.store = new this.options.field_store_class(this.options.fieldid, store_opts);

        this.store.getOptions();

        map.pm.setLang('pt_br');

        map.pm.addControls({
            position: 'topleft',
            drawCircle: true,
            drawCircleMarker: false,
            drawMarker: false,
            drawPolyline: false,
            drawRectangle: true,
            drawPolygon: true,
            cutPolygon: false,
            removalMode: true,
        });

        let self = this;
        let draw_layer = null;

        map.on('pm:create', function (e) {

            draw_layer = e.layer;

            var type = e.shape;
            var layer = e.layer;
            if (type === 'Circle') {
                var origin = layer.getLatLng(); //center of drawn circle
                var radius = layer.getRadius(); //radius of drawn circle
                var projection = L.CRS.EPSG4326;
                var polys = createGeodesicPolygon(origin, radius, 60, 0, projection); //these are the points that make up the circle
                var polygon = []; // store the geometry
                for (var i = 0; i < polys.length; i++) {
                    var geometry = [polys[i].lat, polys[i].lng];
                    polygon.push(geometry);
                }

                self.store.clear();
                var polyCircle = L.polygon(polygon).addTo(map);
                draw_layer = polyCircle;
                map.removeLayer(e.layer);
            }

            self.store.save(draw_layer);

            draw_layer.on('pm:edit', function (e) {
                self.store.save(draw_layer);
            });
        });

        map.on('pm:drawstart', function () {
            if (draw_layer) {
                map.removeLayer(draw_layer);
                draw_layer = null;
                self.store.clear();
            }
        });

        map.on('pm:remove', function () {
            draw_layer = null;
            self.store.clear();
        });

        // Load
        let value = this.store.load();
        if(value) {

            let geometry_obj = JSON.parse(value);
            draw_layer = L.geoJSON(
                {'type': 'Feature', 'properties': {}, 'geometry': geometry_obj},
                { pmIgnore: false }
            ).addTo(map);

            map.fitBounds(draw_layer.getBounds());

            let final_layer = null;
            draw_layer.eachLayer(function(l) {
                final_layer = l;
            });

            draw_layer = final_layer;
            self.store.save(draw_layer);
            draw_layer.on('pm:edit', function (e) {
                self.store.save(draw_layer);
            });
        }

    },

    load: function(map, draw_layer) {

        let value = this.store.load();

        if(value) {

            let geometry_obj = JSON.parse(value);

            draw_layer = L.geoJSON(
                {'type': 'Feature', 'properties': {}, 'geometry': geometry_obj},
                { pmIgnore: false }
            ).addTo(map);

            self.store.save(draw_layer);

            draw_layer.on('pm:edit', function (e) {
                self.store.save(draw_layer);
            });
        }
    }
});