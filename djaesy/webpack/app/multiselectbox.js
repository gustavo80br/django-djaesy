



;(function() {

    $(document).ready(function() {

        $.fn.select2.amd.require(['select2/utils'], function (Utils) {

            $('[data-autocomplete-light-function=your-autocomplete-function]').on(
                'autocompleteLightInitialize',
                function() {

                    var element = $(this);

                    // Templating helper
                    function template(text, is_html) {
                        if (is_html) {
                            var $result = $('<span>');
                            $result.html(text);
                            return $result;
                        } else {
                            return text;
                        }
                    }

                    function result_template(item) {
                        var text = template(item.text,
                            element.attr('data-html') !== undefined || element.attr('data-result-html') !== undefined
                        );

                        if (item.create_id) {
                            return $('<span></span>').text(text).addClass('dal-create');
                        } else {
                            return $(`<span data-value="${item.id}"></span>`).text(text);
                        }
                    }

                    function selected_template(item) {
                        if (item.selected_text !== undefined) {
                            return template(item.selected_text,
                                element.attr('data-html') !== undefined || element.attr('data-selected-html') !== undefined
                            );
                        } else {
                            return result_template(item);
                        }
                        return
                    }

                    var ajax = null;
                    if ($(this).attr('data-autocomplete-light-url')) {
                        ajax = {
                            url: $(this).attr('data-autocomplete-light-url'),
                            dataType: 'json',
                            delay: 250,

                            data: function (params) {
                                var data = {
                                    q: params.term, // search term
                                    page: params.page,
                                    create: element.attr('data-autocomplete-light-create') && !element.attr('data-tags'),
                                    forward: yl.getForwards(element)
                                };

                                return data;
                            },
                            processResults: function (data, page) {
                                if (element.attr('data-tags')) {
                                    $.each(data.results, function(index, value) {
                                        value.id = value.text;
                                    });
                                }
                                return data;
                            },
                            cache: true
                        };
                    }

                    var list = $(this).select2({
                        tokenSeparators: element.attr('data-tags') ? [','] : null,
                        debug: true,
                        containerCssClass: ':all:',
                        placeholder: element.attr('data-placeholder') || '',
                        language: element.attr('data-autocomplete-light-language'),
                        minimumInputLength: element.attr('data-minimum-input-length') || 0,
                        allowClear: false,
                        closeOnSelect: false,
                        dontBlockScroll: true,
                        multiSelectBox: true,
                        dropdownParent: $(this).closest('div'),
                        dropdownAutoWidth: true,
                        dropdownMinWidth: false,
                        templateResult: result_template,
                        templateSelection: selected_template,
                        ajax: ajax,
                        tags: Boolean(element.attr('data-tags')),
                    }).on("select2:closing", function(e) {
                        e.preventDefault();
                    }).on("select2:closed", function(e) {
                        list.select2("open");
                    });

                    list.select2("open");

                    list.reset = function() {
                        if(ajax) {
                            list.empty();
                            select2_search.val('');
                            select2_search.trigger('keyup');
                            list.trigger('change.select2');
                            update_selected();
                        } else {
                            list.val('');
                            list.trigger('change');
                            select2_search.val('');
                            select2_search.trigger('keyup');
                        }
                    };

                    list.on('multiselectbox:reset', list.reset);

                    let container = list.closest('div');
                    container.addClass('multiselectbox');

                    container.prepend(`
                        <div class="multiselectbox-controls">
                             <div class="form-row align-items-center justify-content-between">
                                <div class="form-group col-auto mb-0">
                                    <div class="form-row align-items-center justify-content-between">
                                        <div class="form-group col-md-auto">
                                            <input class="search_field textinput textInput form-control" type="search" tabindex="0" autocomplete="off" autocorrect="off" autocapitalize="none" spellcheck="false" role="searchbox" aria-autocomplete="list" placeholder="${element.attr('data-placeholder')}">
                                        </div>
                                        <div class="form-group col-md-auto">
                                            <a href="#" class="btn btn-sm btn-mdi btn-primary multiselectbox-selectall" class="multiselectbox-selectall">${MULTIBOX_SELECT_BUTTON} <i class="mdi mdi-chevron-double-right"></i></a> ${MULTIBOX_HELP_TEXT}
                                        </div>
                                    </div>
                                </div>
                                <div class="form-group col-auto mb-0">
                                    <div class="form-group col-md-auto">
                                        <span class="multiselectbox-selected-count"></span>
                                    </div>
                                </div>
                                <div class="form-group col-auto mb-0">
                                    <div class="form-row align-items-center justify-content-between">
                                        <div class="form-group col-md-auto">
                                            <a href="#" class="btn btn-sm btn-mdi btn-secondary multiselectbox-clear"><i class="mdi mdi-chevron-double-left"></i> ${MULTIBOX_CLEAR_BUTTON}</a>
                                        </div>
                                    </div>
                                </div>
                             </div>
                             <div class="prev-results-cache" style="display:none;"></div>
                        </div>
                    `);

                    function update_selected() {
                        let selected = list.select2('data').length;
                        let text = `${selected} ${MULTIBOX_SELECTED_PLURAL}`;
                        if(selected === 1) {
                            text = `${selected} ${MULTIBOX_SELECTED_SINGLE}`;
                        } else if(selected === 0) {
                            text = '';
                        }
                        multiselectbox.find('.multiselectbox-selected-count').text(text);
                    }

                    let multiselectbox = element.parent();
                    let select2_search = multiselectbox.find('.select2-search__field');
                    let search_field = multiselectbox.find('.search_field');
                    let result_area = multiselectbox.find('.select2-results__options');
                    let pre_results_cache = multiselectbox.find('.prev-results-cache');
                    let time = null;
                    let last_unfiltered_params = null;

                    let sync_inputs = function() {
                        let val = $(this).val();
                        if(!val && ajax) {
                            select2_search.val(val);
                            list.data('select2').results.lastParams = last_unfiltered_params;
                            list.data('select2').results.lastParams.term = '';
                            let prev_results = pre_results_cache.find(".select2-results__option").not('.select2-results__option--load-more');
                            result_area.find(".select2-results__option").remove();
                            result_area.append(prev_results);
                            result_area.append(list.data('select2').results.$loadingMore[0]);
                        } else {
                            select2_search.val(val);
                            select2_search.trigger('keyup');
                        }
                    };

                    search_field.on('keyup', sync_inputs);
                    search_field.on('search', sync_inputs);

                    search_field.on('focusin', function() {
                        if(ajax) {
                            let val = $(this).val();
                            if (!val) {
                                last_unfiltered_params = list.data('select2').results.lastParams;
                                let actual_options = list.parent().find('.select2-results .select2-results__option').clone();
                                pre_results_cache.empty();
                                pre_results_cache.append(actual_options);
                            }
                        }
                    });

                    multiselectbox.find('.multiselectbox-clear').on('click', list.reset);

                    multiselectbox.find('.multiselectbox-selectall').on('click', function() {

                        let ids = [];

                        list.parent().find('.select2-results .select2-results__option[aria-selected="false"]').each(
                            function() {
                                if(String(this.id).includes('-')) {
                                    ids.push(String(this.id).split('-').pop());
                                } else {
                                    let data = Utils.GetData(this, 'data');
                                    ids.push(data);
                                }
                            }
                        );
                        if(ids.length > 0) {

                            if(ajax) {
                                let el_str = '';
                                ids.forEach(function (item, idx) {
                                    el_str += `<option value="${item.id}" selected>${item.selected_text}</option>`;
                                });
                                list.append(el_str);
                                list.parent().find('.select2-results .select2-results__option[aria-selected="false"]').attr('aria-selected', true);

                                let val_ids = [];
                                ids.forEach(function (item) {
                                    val_ids.push(item.id);
                                });

                                list.trigger('change');
                            } else {
                                list.val(ids);
                                list.trigger('change');
                                select2_search.val('');
                                select2_search.trigger('keyup');
                            }
                        }
                    });

                    list.on('change', function() {
                        clearTimeout(time);
                        update_selected();
                        time = setTimeout(function() {
                            if(ajax) { result_area.trigger('scroll'); }
                        }, 100);
                    });

                    $(this).on('select2:selecting', function (e) {
                        var data = e.params.args.data;

                        if (data.create_id !== true)
                            return;

                        e.preventDefault();

                        var select = $(this);

                        $.ajax({
                            url: $(this).attr('data-autocomplete-light-url'),
                            type: 'POST',
                            dataType: 'json',
                            data: {
                                text: data.id,
                                forward: yl.getForwards($(this))
                            },
                            beforeSend: function(xhr, settings) {
                                xhr.setRequestHeader("X-CSRFToken", document.csrftoken);
                            },
                            success: function(data, textStatus, jqXHR ) {
                                select.append(
                                    $('<option>', {value: data.id, text: dametata.text, selected: true})
                                );
                                select.trigger('change');
                            }
                        });
                    });
                }
            );

            $('[data-autocomplete-light-function]:not(.select2-hidden-accessible)').trigger('autocompleteLightInitialize');

        });

    });

}.call(this));