'use strict';

$(document).ready(function() {
    var summary_loaded = false;

    /* Callback a function when an element comes in view */
    function callback_in_view(element, func) {
        function handler(evt) {
            var visible = (
                $('#summarygrid-display').css('display') != 'none' &&
                (element.offset().top <= $(window).height() + $(window).scrollTop()) &&
                    (element.offset().top + element.height() >= $(window).scrollTop()));
            if (visible) {
                func();
                $(window).off('scroll', handler);
            }
        }
        $(window).on('scroll', handler);
    }

    function get_benchmarks_by_groups() {
        var main_json = $.asv.main_json;
        var groups = {};
        $.each(main_json.benchmarks, function(bm_name, bm) {
            var i = bm_name.indexOf('.');
            var group = bm_name.slice(0, i);
            var name = bm_name.slice(i + 1);
            if (groups[group] === undefined) {
                groups[group] = [];
            }
            groups[group].push(bm_name);
        });
        return groups;
    }

    function benchmark_container(bm) {
        var container = $(
            '<a class="btn benchmark-container" href="#' + bm.name +
            '"/>');
        var plot_div = $(
            '<div id="summarygrid-' + bm.name + '" class="benchmark-plot"/>');
        var display_name = bm.pretty_name || bm.name.slice(bm.name.indexOf('.') + 1);
        var name = $('<div class="benchmark-text">' + display_name + '</div>');
        name.tooltip({
            title: bm.name,
            html: true,
            placement: 'top',
            container: 'body',
            animation: false
        });

        plot_div.tooltip({
            title: bm.code,
            html: true,
            placement: 'bottom',
            container: 'body',
            animation: false
        });

        container.append(name);
        container.append(plot_div);

        callback_in_view(plot_div, function() {
            $.asv.load_graph_data(
                'graphs/summary/' + bm.name + '.json'
            ).done(function(data) {
                var options = {
                    colors: $.asv.colors,
                    series: {
                        lines: {
                            show: true,
                            lineWidth: 2
                        },
                        shadowSize: 0
                    },
                    grid: {
                        borderWidth: 1,
                        margin: 0,
                        labelMargin: 0,
                        axisMargin: 0,
                        minBorderMargin: 0
                    },
                    xaxis: {
                        ticks: [],
                    },
                    yaxis: {
                        ticks: [],
                        min: 0
                    },
                    legend: {
                        show: false
                    }
                };

                var plot = $.plot(
                    plot_div, [{data: data}], options);
            }).fail(function() {
                // TODO: Handle failure
            });
        });
        return container;
    }

    function make_summary() {
        var summary_display = $('#summarygrid-display');
        var main_json = $.asv.main_json;
        var summary_container = $('<div/>');

        if (summary_loaded) {
            return;
        }

        $.each(get_benchmarks_by_groups(), function(group, benchmarks) {
            var group_container = $('<div class="benchmark-group"/>')
            group_container.attr('id', 'group-' + group)
            group_container.append($('<h1>' + group + '</h1>'));
            summary_display.append(group_container);
            $.each(benchmarks, function(i, bm_name) {
                var bm = $.asv.main_json.benchmarks[bm_name];
                group_container.append(benchmark_container(bm));
            });
        });

        summary_display.append(summary_container);
        $(window).trigger('scroll');

        summary_loaded = true;
    }

    $.asv.register_page('', function(params) {
        $('#summarygrid-display').show();
        $("#title").text("All benchmarks");
        $('.tooltip').remove();
        make_summary();
    });
});
