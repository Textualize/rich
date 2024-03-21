'use strict';

$(document).ready(function() {
    /* GLOBAL STATE */
    /* The index.json content as returned from the server */
    var main_timestamp = '';
    var main_json = {};
    /* Extra pages: {name: show_function} */
    var loaded_pages = {};
    /* Previous window scroll positions */
    var window_scroll_positions = {};
    /* Previous window hash location */
    var window_last_location = null;
    /* Graph data cache */
    var graph_cache = {};
    var graph_cache_max_size = 5;

    var colors = [
        '#247AAD',
        '#E24A33',
        '#988ED5',
        '#777777',
        '#FBC15E',
        '#8EBA42',
        '#FFB5B8'
    ];

    var time_units = [
        ['ps', 'picoseconds', 0.000000000001],
        ['ns', 'nanoseconds', 0.000000001],
        ['μs', 'microseconds', 0.000001],
        ['ms', 'milliseconds', 0.001],
        ['s', 'seconds', 1],
        ['m', 'minutes', 60],
        ['h', 'hours', 60 * 60],
        ['d', 'days', 60 * 60 * 24],
        ['w', 'weeks', 60 * 60 * 24 * 7],
        ['y', 'years', 60 * 60 * 24 * 7 * 52],
        ['C', 'centuries', 60 * 60 * 24 * 7 * 52 * 100]
    ];

    var mem_units = [
        ['', 'bytes', 1],
        ['k', 'kilobytes', 1000],
        ['M', 'megabytes', 1000000],
        ['G', 'gigabytes', 1000000000],
        ['T', 'terabytes', 1000000000000]
    ];

    function pretty_second(x) {
        for (var i = 0; i < time_units.length - 1; ++i) {
            if (Math.abs(x) < time_units[i+1][2]) {
                return (x / time_units[i][2]).toFixed(3) + time_units[i][0];
            }
        }

        return 'inf';
    }

    function pretty_byte(x) {
        for (var i = 0; i < mem_units.length - 1; ++i) {
            if (Math.abs(x) < mem_units[i+1][2]) {
                break;
            }
        }
        if (i == 0) {
            return x + '';
        }
        return (x / mem_units[i][2]).toFixed(3) + mem_units[i][0];
    }

    function pretty_unit(x, unit) {
        if (unit == "seconds") {
            return pretty_second(x);
        }
        else if (unit == "bytes") {
            return pretty_byte(x);
        }
        else if (unit && unit != "unit") {
            return '' + x.toPrecision(3) + ' ' + unit;
        }
        else {
            return '' + x.toPrecision(3);
        }
    }

    function pad_left(s, c, num) {
        s = '' + s;
        while (s.length < num) {
            s = c + s;
        }
        return s;
    }

    function format_date_yyyymmdd(date) {
        return (pad_left(date.getFullYear(), '0', 4)
                + '-' + pad_left(date.getMonth() + 1, '0', 2)
                + '-' + pad_left(date.getDate(), '0', 2));
    }

    function format_date_yyyymmdd_hhmm(date) {
        return (format_date_yyyymmdd(date) + ' '
                + pad_left(date.getHours(), '0', 2)
                + ':' + pad_left(date.getMinutes(), '0', 2));
    }

    /* Convert a flat index to permutation to the corresponding value */
    function param_selection_from_flat_idx(params, idx) {
        var selection = [];
        if (idx < 0) {
            idx = 0;
        }
        for (var k = params.length-1; k >= 0; --k) {
            var j = idx % params[k].length;
            selection.unshift([j]);
            idx = (idx - j) / params[k].length;
        }
        selection.unshift([null]);
        return selection;
    }

    /* Convert a benchmark parameter value from their native Python
       repr format to a number or a string, ready for presentation */
    function convert_benchmark_param_value(value_repr) {
        var match = Number(value_repr);
        if (!isNaN(match)) {
            return match;
        }

        /* Python str */
        match = value_repr.match(/^'(.+)'$/);
        if (match) {
            return match[1];
        }

        /* Python unicode */
        match = value_repr.match(/^u'(.+)'$/);
        if (match) {
            return match[1];
        }

        /* Python class */
        match = value_repr.match(/^<class '(.+)'>$/);
        if (match) {
            return match[1];
        }

        return value_repr;
    }

    /* Convert loaded graph data to a format flot understands, by
       treating either time or one of the parameters as x-axis,
       and selecting only one value of the remaining axes */
    function filter_graph_data(raw_series, x_axis, other_indices, params) {
        if (params.length == 0) {
            /* Simple time series */
            return raw_series;
        }

        /* Compute position of data entry in the results list,
           and stride corresponding to plot x-axis parameter */
        var stride = 1;
        var param_stride = 0;
        var param_idx = 0;
        for (var k = params.length - 1; k >= 0; --k) {
            if (k == x_axis - 1) {
                param_stride = stride;
            }
            else {
                param_idx += other_indices[k + 1] * stride;
            }
            stride *= params[k].length;
        }

        if (x_axis == 0) {
            /* x-axis is time axis */
            var series = new Array(raw_series.length);
            for (var k = 0; k < raw_series.length; ++k) {
                if (raw_series[k][1] === null) {
                    series[k] = [raw_series[k][0], null];
                } else {
                    series[k] = [raw_series[k][0],
                                 raw_series[k][1][param_idx]];
                }
            }
            return series;
        }
        else {
            /* x-axis is some parameter axis */
            var time_idx = null;
            if (other_indices[0] === null) {
                time_idx = raw_series.length - 1;
            }
            else {
                /* Need to search for the correct time value */
                for (var k = 0; k < raw_series.length; ++k) {
                    if (raw_series[k][0] == other_indices[0]) {
                        time_idx = k;
                        break;
                    }
                }
                if (time_idx === null) {
                    /* No data points */
                    return [];
                }
            }

            var x_values = params[x_axis - 1];
            var series = new Array(x_values.length);
            for (var k = 0; k < x_values.length; ++k) {
                if (raw_series[time_idx][1] === null) {
                    series[k] = [convert_benchmark_param_value(x_values[k]),
                                 null];
                }
                else {
                    series[k] = [convert_benchmark_param_value(x_values[k]),
                                 raw_series[time_idx][1][param_idx]];
                }
                param_idx += param_stride;
            }
            return series;
        }
    }

    function filter_graph_data_idx(raw_series, x_axis, flat_idx, params) {
        var selection = param_selection_from_flat_idx(params, flat_idx);
        var flat_selection = [];
        $.each(selection, function(i, v) {
            flat_selection.push(v[0]);
        });
        return filter_graph_data(raw_series, x_axis, flat_selection, params);
    }

    /* Escape special characters in graph item file names.
       The implementation must match asv.util.sanitize_filename */
    function sanitize_filename(name) {
        var bad_re = /[<>:"\/\\^|?*\x00-\x1f]/g;
        var bad_names = ["CON", "PRN", "AUX", "NUL", "COM1", "COM2", "COM3",
                         "COM4", "COM5", "COM6", "COM7", "COM8", "COM9", "LPT1",
                         "LPT2", "LPT3", "LPT4", "LPT5", "LPT6", "LPT7", "LPT8",
                         "LPT9"];
        name = name.replace(bad_re, "_");
        if (bad_names.indexOf(name.toUpperCase()) != -1) {
            name = name + "_";
        }
        return name;
    }

    /* Given a specific group of parameters, generate the URL to
       use to load that graph.
       The implementation must match asv.graph.Graph.get_file_path
     */
    function graph_to_path(benchmark_name, state) {
        var parts = [];
        $.each(state, function(key, value) {
            var part;
            if (value === null) {
                part = key + "-null";
            } else if (value) {
                part = key + "-" + value;
            } else {
                part = key;
            }
            parts.push(sanitize_filename('' + part));
        });
        parts.sort();
        parts.splice(0, 0, "graphs");
        parts.push(sanitize_filename(benchmark_name));

        /* Escape URI components */
        parts = $.map(parts, function (val) { return encodeURIComponent(val); });
        return parts.join('/') + ".json";
    }

    /*
      Load and cache graph data (on javascript side)
     */
    function load_graph_data(url, success, failure) {
        var dfd = $.Deferred();
        if (graph_cache[url]) {
            setTimeout(function() {
                dfd.resolve(graph_cache[url]);
            }, 1);
        }
        else {
            $.ajax({
                url: url + '?timestamp=' + $.asv.main_timestamp,
                dataType: "json",
                cache: true
            }).done(function(data) {
                if (Object.keys(graph_cache).length > graph_cache_max_size) {
                    $.each(Object.keys(graph_cache), function (i, key) {
                        delete graph_cache[key];
                    });
                }
                graph_cache[url] = data;
                dfd.resolve(data);
            }).fail(function() {
                dfd.reject();
            });
        }
        return dfd.promise();
    }

    /*
      Parse hash string, assuming format similar to standard URL
      query strings
    */
    function parse_hash_string(str) {
        var info = {location: [''], params: {}};

        if (str && str[0] == '#') {
            str = str.slice(1);
        }
        if (str && str[0] == '/') {
            str = str.slice(1);
        }

        var match = str.match(/^([^?]*?)\?/);
        if (match) {
            info['location'] = decodeURIComponent(match[1]).replace(/\/+/, '/').split('/');
            var rest = str.slice(match[1].length+1);
            var parts = rest.split('&');
            for (var i = 0; i < parts.length; ++i) {
                var part = parts[i].split('=');
                if (part.length != 2) {
                    continue;
                }
                var key = decodeURIComponent(part[0].replace(/\+/g, " "));
                var value = decodeURIComponent(part[1].replace(/\+/g, " "));
                if (value == '[none]') {
                    value = null;
                }
                if (info['params'][key] === undefined) {
                    info['params'][key] = [value];
                }
                else {
                    info['params'][key].push(value);
                }
            }
        }
        else {
            info['location'] = decodeURIComponent(str).replace(/\/+/, '/').split('/');
        }
        return info;
    }

    /*
      Generate a hash string, inverse of parse_hash_string
    */
    function format_hash_string(info) {
        var parts = info['params'];
        var str = '#' + info['location'];

        if (parts) {
            str = str + '?';
            var first = true;
            $.each(parts, function (key, values) {
                $.each(values, function (idx, value) {
                    if (!first) {
                        str = str + '&';
                    }
                    if (value === null) {
                        value = '[none]';
                    }
                    str = str + encodeURIComponent(key) + '=' + encodeURIComponent(value);
                    first = false;
                });
            });
        }
        return str;
    }

    /*
      Dealing with sub-pages
     */

    function show_page(name, params) {
        if (loaded_pages[name] !== undefined) {
	    $("#nav ul li.active").removeClass('active');
	    $("#nav-li-" + name).addClass('active');
            $("#graph-display").hide();
            $("#summarygrid-display").hide();
            $("#summarylist-display").hide();
            $('#regressions-display').hide();
            $('.tooltip').remove();
            loaded_pages[name](params);
            return true;
        }
        else {
            return false;
        }
    }

    function hashchange() {
        var info = parse_hash_string(window.location.hash);

        /* Keep track of window scroll position; makes the back-button work */
        var old_scroll_pos = window_scroll_positions[info.location.join('/')];
        window_scroll_positions[window_last_location] = $(window).scrollTop();
        window_last_location = info.location.join('/');

        /* Redirect to correct handler */
        if (show_page(info.location, info.params)) {
            /* show_page does the work */
        }
        else {
            /* Display benchmark page */
            info.params['benchmark'] = info.location[0];
            show_page('graphdisplay', info.params);
        }

        /* Scroll back to previous position, if any */
        if (old_scroll_pos !== undefined) {
            $(window).scrollTop(old_scroll_pos);
        }
    }

    function get_commit_hash(revision) {
        var commit_hash = main_json.revision_to_hash[revision];
        if (commit_hash) {
            // Return printable commit hash
            commit_hash = commit_hash.slice(0, main_json.hash_length);
        }
        return commit_hash;
    }

    function get_revision(commit_hash) {
        var rev = null;
        $.each(main_json.revision_to_hash, function(revision, full_commit_hash) {
            if (full_commit_hash.startsWith(commit_hash)) {
                rev = revision;
                // break the $.each loop
                return false;
            }
        });
        return rev;
    }

    function init_index() {
        /* Fetch the main index.json and then set up the page elements
           based on it. */
        $.ajax({
            url: "index.json" + '?timestamp=' + $.asv.main_timestamp,
            dataType: "json",
            cache: true
        }).done(function (index) {
            main_json = index;
            $.asv.main_json = index;

            /* Page title */
            var project_name = $("#project-name")[0];
            project_name.textContent = index.project;
            project_name.setAttribute("href", index.project_url);
            $("#project-name").textContent = index.project;
            document.title = "airspeed velocity of an unladen " + index.project;

            $(window).on('hashchange', hashchange);

            $('#graph-display').hide();
            $('#regressions-display').hide();
            $('#summarygrid-display').hide();
            $('#summarylist-display').hide();

            hashchange();
        }).fail(function () {
            $.asv.ui.network_error();
        });
    }

    function init() {
        /* Fetch the info.json */
        $.ajax({
            url: "info.json",
            dataType: "json",
            cache: false
        }).done(function (info) {
            main_timestamp = info['timestamp'];
            $.asv.main_timestamp = main_timestamp;
            init_index();
        }).fail(function () {
            $.asv.ui.network_error();
        });
    }


    /*
      Set up $.asv
     */

    this.register_page = function(name, show_function) {
        loaded_pages[name] = show_function;
    }
    this.parse_hash_string = parse_hash_string;
    this.format_hash_string = format_hash_string;

    this.filter_graph_data = filter_graph_data;
    this.filter_graph_data_idx = filter_graph_data_idx;
    this.convert_benchmark_param_value = convert_benchmark_param_value;
    this.param_selection_from_flat_idx = param_selection_from_flat_idx;
    this.graph_to_path = graph_to_path;
    this.load_graph_data = load_graph_data;
    this.get_commit_hash = get_commit_hash;
    this.get_revision = get_revision;

    this.main_timestamp = main_timestamp; /* Updated after info.json loads */
    this.main_json = main_json; /* Updated after index.json loads */

    this.format_date_yyyymmdd = format_date_yyyymmdd;
    this.format_date_yyyymmdd_hhmm = format_date_yyyymmdd_hhmm;
    this.pretty_unit = pretty_unit;
    this.time_units = time_units;
    this.mem_units = mem_units;

    this.colors = colors;

    $.asv = this;


    /*
      Launch it
     */

    init();
});
