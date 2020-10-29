// import 'leaflet-markercluster/markercluster.css'
// import 'leaflet-markercluster/markercluster.default.css'
// import 'leaflet-search/dist/leaflet-search.min.css'
import axios from 'axios'
import toastr from "toastr";

export class VehicleMap {

    static init_map(map, options, geojson, geojson_events) {

        // --

        let size_invalidate_timer = null;

        let track_layers = {};
        let markers_layers = {};
        let event_layers = {};

        let active_tracks = [];

        let animate_fitbounds = false;
        const max_zoom_to_fitbounds = 18;
        const max_zoom_to_event = 18;

        // let geojson = {};
        //
        // let csrf_token = $('input[name="csrfmiddlewaretoken"]').val();

        // $.ajax({
        //     url: `/api/v1/monitoring/track/`,
        //     method: 'POST',
        //     data: {
        //         vehicle: 1492
        //     },
        //     success: function (data) {
        //         geojson = data
        //     },
        //     error: function (error) {
        //         console.log(error);
        //     }
        // });

        // let data = {
        //     vehicle: 1492
        // };
        //
        // const url = '/api/v1/monitoring/track/';
        // const config = {headers: {"X-CSRFToken": csrf_token}};

        function fixLayerNativeZoom() {
            let mapLayer = Object.values(map._layers).find(layer => layer._url !== undefined);
            if (!mapLayer.options.fixed) {
                mapLayer.options.maxNativeZoom = mapLayer.options.maxZoom;
                mapLayer.options.maxZoom = 22;
            }
            mapLayer.options.fixed = true;
        }

        function vehicleIcon(feature, special, image=null) {

            const { properties } = feature;

            if (properties['vehicle_image'] && properties['vehicle_image'].length != 0) {
                image = properties['vehicle_image'];
            } else if (properties['model_image'] && properties['model_image'].length != 0) {
                image = properties['model_image'];
            } else if (properties['type_image'] && properties['type_image'].length != 0) {
                image = properties['type_image'];
            }

            let moving = 'not-moving';
            let engine = 'engine-off';

            let content = '';

            if(image) {
                content = `<img src="${image}" width="32"/>`;
            } else if(special === 'start' && feature.track_id) {
                content = `<h6 class="mb-0 pl-2 pr-2 pb-1 pt-1 text-nowrap">${feature.track_id}  <i class="mdi mdi-near-me"></i></h6>`;
            } else if(special === 'end' && feature.track_id) {
                content = `<h6 class="mb-0 pl-2 pr-2 pb-1 pt-1 text-nowrap">${feature.track_id}  <i class="mdi mdi-flag-checkered"></i></h6>`;
            }

            if(content) {
                content = `
                    <div class="marker-pointer"></div>
                    <div class="marker-content">
                        ${content}
                    </div>
                `;
            }

            // Rotating effect
            //<div class="marker-dot ${delay} ${moving} ${engine}"></div>
            let html = `
                <div class="map-marker">
                    <div class="marker-dot ${engine}"></div>
                    ${content}
                </div>
            `;

            let icon = L.divIcon({
                className: '',
                html: html,
                iconSize: [30, 42],
                iconAnchor: [0, 0]
            });

            return icon;
        }

        function markerIcon(feature, special) {
            const {moving, engine} = feature.properties;

            let className;
            if (engine)
                className = 'marker-engine'
            else if (moving)
                className = 'marker-moving'
            else
                className = 'marker-stopped'
            let html;
            if (special == 'start') {
                html = '<span class="mdi mdi-24px mdi-flag-variant"></span>'
            } else if (special == 'end') {
                html = '<span class="mdi mdi-24px mdi-car-side"></span>'
            } else {
                html = '<span class="mdi mdi-24px mdi-map-marker"></span>'
            }

            let dot = `
                <div class="map-marker">
                    <div class="marker-dot"></div>
                </div>
            `;

            return L.divIcon({
                className: className,
                html: html,
                iconSize: [30, 42],
                iconAnchor: [12, 24]
            })
        }

        function markerTooltipHtml(data, track_id, track_data, special) {
            let original_data = data;
            data = data.properties;
            if (special) {
                let specialMsg = special == 'start' ? 'Partida' : special == 'end' ? 'Chegada' : ''
                let date = special == 'start' ? track_data['start_date'] : track_data['end_date']
                let duration = `${Math.floor(track_data.duration / 60)}h${Math.round(track_data.duration % 60)}min`
                let distance = Math.round(track_data.distance * 100000) / 100
                let hourmeter = Math.round(track_data['hour_meter'] * 100) / 100
                let odometer = Math.round(track_data['odometer'] * 100) / 100

                return `
                    <div style="padding: 0px 12px; min-width: 260px; max-height: 200px;">
                        <div class="row pt-1 pl-1">
                            <h5 class="mb-0">Percurso #${track_id} - ${specialMsg}</h>
                        </div>
                        <div class="row pl-1">
                            ${date}
                        </div>
                        <div class="row mt-1">
                            <div class="info-container">
                                <div class="info slim">
                                    <label class="info-label">Duração</label>
                                    <span>${duration}</span>
                                </div>
                                <div class="info slim">
                                    <label class="info-label">Distância</label>
                                    <span>${distance} km</span>
                                </div>
                                <div class="info slim">
                                    <label class="info-label">Horímetro</label>
                                    <span>${hourmeter} h</span>
                                </div>
                                <div class="info slim">
                                    <label class="info-label">Odômetro</label>
                                    <span>${odometer} km</span>
                                </div>
                            </div>
                        </div>
                    </div>`;

            } else {
                let engine = '';
                if (data.engine) {
                    engine = '<i class="mdi mdi-24px status-icon mdi-key-variant success-ic"></i>';
                } else {
                    engine = '<i class="mdi mdi-24px status-icon mdi-key-variant grey-ic"></i>';
                }

                let moving = '';
                if (data.moving) {
                    moving = '<i class="mdi mdi-24px status-icon mdi-truck-fast success-ic"></i>';
                } else {
                    moving = '<i class="mdi mdi-24px status-icon mdi-car-brake-parking grey-ic"></i>';
                }

                let engineTime = data['motor_state_timer']
                let engineTimeMinutes = (engineTime % 60).toString().padStart(2, '0')
                let engineTimeHours = Math.floor(engineTime / 60).toString().padStart(2, '0')

                return `
                    <div style="padding: 0px 12px; min-width: 260px; max-height: 200px;">
                        <div class="row">
                            <div class="col col-7 pl-4">
                                <div class="row pt-1">
                                    <h5 class="mb-0">Percurso #${track_id}</h>
                                </div>
                                ${data.datetime ? `<div class="row">
                                    ${data.datetime}
                                </div>` : ''}
                            </div>
                            <div class="col col-5">
                                ${engine} ${moving}
                            </div>
                        </div>
                        <div class="row mt-1">
                            <div class="info-container">
                                ${data.moving && data.speed > 0 ? `<div class="info slim">
                                    <label class="info-label">Velocidade</label>
                                    <span>${data.speed} km/h</span>
                                </div>` : ''}
                                ${track_data.duration ? `<div class="info slim">
                                    <label class="info-label">Tempo motor ${data.engine ? 'ligado' : 'desligado'}</label>
                                    <span>${engineTimeHours}h${engineTimeMinutes}min</span>
                                </div>` : ''}
                            </div>
                        </div>
                    </div>`;
            }
        }

        function pointToMarker(track_id, track) {

            let track_size = track.coordinates;
            if(!track_size) {
                track_size = track.features.length;
            } else {
                track_size = track_size.length;
            }

            let track_counter = 1;
            let oldest_track = Math.min(...active_tracks);
            let latest_track = Math.max(...active_tracks);
            let track_data = track.properties;

            return function(feature, latlng) {

                let icon;
                let special = null;

                if(track_data.vehicle_image !== undefined) {
                    icon = vehicleIcon(feature, 'latest', track_data.vehicle_image);
                } else if(track_counter === 1) {
                    feature.track_id = track_id;
                    special = 'start';
                    icon = vehicleIcon(feature, 'start');
                } else if(track_counter === track_size && track_id > latest_track) {
                    feature.track_id = track_id;
                    special = 'end'
                    icon = vehicleIcon(feature, 'end');
                } else {
                    icon = markerIcon(feature);
                }

                const tooltip = markerTooltipHtml(feature, track_id, track_data, special);

                track_counter += 1;

                const layer = L.marker(latlng, {icon: icon, radius: 8});

                layer.bindTooltip(() => tooltip, {direction: 'top', opacity: 1, offset: [0, -12]});
                return layer
            }
        }

        function buildGeojsonLayer(map_data, track_id) {
            if (map_data.properties) {
                return L.geoJson(map_data, {
                    pointToLayer: pointToMarker(track_id, map_data)
                });
            } else {
                return L.geoJson(
                    map_data,
                    {
                        style: () => ({
                            color: '#787a7b'
                        })
                    }
                );
            }
        }

        function setTheControlsForTheHartOfTheSun() {

            map.zoomControl.setPosition('topleft');
            map.layerscontrol.setPosition('bottomright');

            map.addControl(map.zoomControl);
            map.removeControl(map.resetviewControl);
            map.addControl(map.layerscontrol);

            L.control.fullscreen({
              position: map.zoomControl.getPosition(),
              content: '<i class="mdi mdi-arrow-expand-all mdi-24px"></i>',
            }).addTo(map);

            (function() {
                var control = new L.Control({position:'topleft'});
                control.onAdd = function(map) {
                    var div = L.DomUtil.create('div', 'leaflet-control-zoom leaflet-bar leaflet-control')
                    var azoom = L.DomUtil.create('a','leaflet-control-zoom-out leaflet-bar-part', div);
                    azoom.innerHTML = '<i class="mdi mdi-map-marker-radius mdi-24px"></i>';
                    div.appendChild(azoom);
                    L.DomEvent
                        .disableClickPropagation(azoom)
                        .addListener(azoom, 'click', function(e) {
                            e.stopPropagation();
                            e.preventDefault();
                            fitMapBounds();
                            return false;
                        }, azoom);
                    return div;
                };
                return control;
            }()).addTo(map);

            $('#go-to-last-pos').on('click', function() {
                $(document).trigger('vehicle-details:go-to-last-pos');
            });
        }

        function getActiveTracksLayers() {
            return $.map(track_layers, function(value, index) {
                if(value !== null) {
                    return [value];
                }
            });
        }

        function getActiveMarkersLayers() {
            return $.map(markers_layers, function(value, index) {
                if(value !== null) {
                    return [value];
                }
            });
        }

        function hideGeojsonLayers(layers) {
            layers.forEach(function(layer) {
                if(!layer.setStyle) {
                    let sublayers = layer.getLayers();
                    hideGeojsonLayers(sublayers);
                } else {
                    layer.setStyle({
                        opacity: '0'
                    });
                }
            });
        }

        function unhideGeojsonLayers(layers) {
            layers.forEach(function(layer) {
                if(!layer.setStyle) {
                    let sublayers = layer.getLayers();
                    unhideGeojsonLayers(sublayers);
                } else {
                    layer.setStyle({
                        opacity: '1'
                    });
                }
            });
        }

        function fitMapBounds(animate=true) {
            let active_layers = getActiveTracksLayers();
            if(active_layers.length > 0) {
                if(animate) {
                    hideGeojsonLayers(active_layers);
                    map.flyToBounds(L.featureGroup(active_layers).getBounds(), {maxZoom: max_zoom_to_fitbounds, padding: [50, 50]});
                    const unhide = function() { unhideGeojsonLayers(active_layers); map.off('zoomend', unhide) };
                    map.on('zoomend', unhide);
                } else {
                    map.fitBounds(L.featureGroup(active_layers).getBounds(), {maxZoom: max_zoom_to_fitbounds, padding: [50, 50]});
                }
            }
        }

        function removeTrackLayer(track_id, fit_bounds=true) {

            let track_to_remove = track_layers[track_id];
            let markers_to_remove = markers_layers[track_id];

            if(track_to_remove && markers_to_remove) {

                map.removeLayer(track_to_remove);
                map.removeLayer(markers_to_remove);
                removeEventsLayer(track_id);

                delete track_layers[track_id];
                delete markers_layers[track_id];

                if(track_id > 0) {
                    let track_id_index = active_tracks.indexOf(track_id);
                    active_tracks.splice(track_id_index,1);
                }

                if(fit_bounds) {
                    fitMapBounds();
                }

                if(active_tracks.length === 0) {
                    let zero_track = buildGeojsonLayer(geojson.features[0].features[0], 0);
                    let zero_markers = buildGeojsonLayer(geojson.features[0].features[1], 0);
                    zero_track.addTo(map);
                    zero_markers.addTo(map);
                    track_layers[0] = zero_track;
                    markers_layers[0] = zero_markers;
                    if(fit_bounds) {
                        fitMapBounds();
                    }
                }

                return true;
            }
            return false;
        }

        function addTrackLayer(track_id, fit_bounds=true) {

            let layer_to_remove_and_add = null;

            if(active_tracks.length > 0 && track_id > 0) {
                let oldest_track = Math.min(...active_tracks);
                let latest_track = Math.max(...active_tracks);
                if(track_id > latest_track && active_tracks.length > 0) {
                    layer_to_remove_and_add = latest_track;
                } else if(track_id < oldest_track && active_tracks.length > 0) {
                    layer_to_remove_and_add = oldest_track;
                }
                removeTrackLayer(layer_to_remove_and_add, fit_bounds);
            }

            let new_track = buildGeojsonLayer(geojson.features[track_id].features[0], track_id);
            let new_markers = buildGeojsonLayer(geojson.features[track_id].features[1], track_id);
            let new_events = addEventsLayer(geojson_events, track_id);

            removeTrackLayer(track_id, fit_bounds);

            track_layers[track_id] = new_track;
            markers_layers[track_id] = new_markers;
            event_layers[track_id] = new_events;

            if(layer_to_remove_and_add) {
                addTrackLayer(layer_to_remove_and_add);
            }

            if(track_id > 0) {
                if(!active_tracks.includes(track_id)) { active_tracks.push(track_id); }
                removeTrackLayer(0, fit_bounds);
            }

            if(fit_bounds) {
                fitMapBounds(false);
            }

            animate_fitbounds = true;
            map.invalidateSize();

            new_events.addTo(map);
            new_markers.addTo(map);
            new_track.addTo(map);

        }

        // --

        function eventMarkerIcon(feature) {

            let className = 'marker-stopped';

            const icon_map = {
                'C': '🔺 ',
                'H': '🟠 ',
                'M': '🟡 ',
                'L': '🟢 ',
                'I': '🔘 ',
            };

            const icon_css = {
                'C': 'critical',
                'H': 'major',
                'M': 'minor',
                'L': 'warning',
                'I': 'info',
            };

            const icon = icon_map[feature.properties.alert__severity];
            const css = icon_css[feature.properties.alert__severity];

            let content = `
                    <div class="marker-pointer"></div>
                    <div class="marker-content">
                        <h5 class="mb-0">${icon}</h5>
                    </div>
                `;

            let html = `
                <div class="map-marker">
                    <div class="event-dot ${css}"></div>
                    ${content}
                </div>
            `;

            return L.divIcon({
                className: className,
                html: html,
                iconSize: [30, 42],
                iconAnchor: [0, 0]
            });
        }

        function eventMarkerTooltipHtml(data, latlgn) {

            const severity_description = {
                'C': '🔺 Crítico',
                'H': '🟠 Alto',
                'M': '🟡 Médio',
                'L': '🟢 Baixo',
                'I': '🔘 Informativo'
            };

            const severity =  severity_description[data.alert__severity];

            return `
                <h5>
                    ${data.alert__name}<br/>
                    <small>${data.event_class__name}</small><br/>
                    <small>${data.date}</small><br/>
                    <small>${severity}</small><br/>
                    <small>Percurso #${data.segment_id}</small><br/>
                </h5>
            `;
        }

        function pointToEventMarker(data, track_id) {

            let track_size = data.coordinates;
            if(!track_size) {
                track_size = data.features.length;
            } else {
                track_size = track_size.length;
            }

            let track_data = data.properties;

            return function(feature, latlng) {

                let icon;

                if(feature.properties.segment_id !== track_id) {
                    return;
                }

                icon = eventMarkerIcon(feature);

                const tooltip = eventMarkerTooltipHtml(feature.properties,  latlng);
                const layer = L.marker(latlng, {icon: icon, radius: 8});

                layer.bindTooltip(() => tooltip, {direction: 'top', opacity: 1, offset: [0, 0]});

                return layer;
            }
        }

        function removeEventsLayer(track_id) {
            if(event_layers[track_id]) {
                map.removeLayer(event_layers[track_id]);
                delete event_layers[track_id];
            }
        }

        function addEventsLayer(event_data, track_id) {
            return L.geoJson(event_data, {
                pointToLayer: pointToEventMarker(event_data, track_id)
            });
        }

        // --

        fixLayerNativeZoom();
        map.on('baselayerchange', fixLayerNativeZoom);

        $(document).on('vehicle-details:track-selection', function(e, selection, fit_bounds) {
            const active = active_tracks.slice();
            active.forEach(function(active_item) {
                if(!selection.includes(active_item.toString())) {
                    removeTrackLayer(active_item, fit_bounds);
                }
            });
            selection.forEach(function(selected_item) {
                let int_item = parseInt(selected_item);
                if(!active_tracks.includes(int_item)) {
                    addTrackLayer(int_item, fit_bounds);
                }
            });
        });

        $(document).on('app-panel:fullscreen app-panel:slider-drag-end app-panel:menubar-toggle app-panel:sidebar-toggle', function() {
            clearTimeout(size_invalidate_timer);
            size_invalidate_timer = setTimeout(() => map.invalidateSize(), 400);
        });

        $(document).on('i3track:select_track', function(e, track_id, point) {
            $(document).trigger('vehicle-details:track-selection', [[track_id], false]);
            $('.track-row.selected').removeClass('selected');
            $(`#Track${track_id}`).addClass('selected');
            map.setView(new L.LatLng(point[0], point[1]), max_zoom_to_event, {animate: true});
        });


        // axios.post(url, data, config)
        //     .then(function (response) {
        //
        //         geojson = JSON.parse(response.data);
        //
        //         addTrackLayer(0);
        //         setTheControlsForTheHartOfTheSun();
        //
        //         setTimeout(() => map.invalidateSize(), 500);
        //
        //         console.log(geojson);
        //         // if (self.silence_form_multiple) {
        //         //     self.notificationsSelected.forEach(function (n) {
        //         //         self.removeNotification(n.id);
        //         //     });
        //         // } else {
        //         //     self.removeNotification(self.silence_form_id);
        //         // }
        //         // -- Switch modal
        //         // $(self.silence_modal).modal('hide');
        //         // -- Notify and finish
        //         // toastr['success']('Operação de silenciar alertas concluída com sucesso!', 'Sucesso');
        //         // self.silence_form_sending = false;
        //     })
        //     .catch(function (error) {
        //         console.log(error);
        //         // -- Notify and finish
        //         // toastr['error']('Houve um erro ao silenciar a alertas! Contate o suporte.', 'Erro');
        //         // self.silence_form_sending = false;
        //     });

        addTrackLayer(0);
        setTheControlsForTheHartOfTheSun();

        setTimeout(() => map.invalidateSize(), 500);

        $(document).trigger('i3track:show_event');

        // ---
    }

}