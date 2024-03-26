'use strict';

$(document).ready(function() {
    function make_panel(nav, heading) {
        var panel = $('<div class="panel panel-default"/>');
        nav.append(panel);
        var panel_header = $(
            '<div class="panel-heading">' + heading + '</div>');
        panel.append(panel_header);
        var panel_body = $('<div class="panel-body"/>');
        panel.append(panel_body);
        return panel_body;
    }

    function make_value_selector_panel(nav, heading, values, setup_callback) {
        var panel_body = make_panel(nav, heading);
        var vertical = false;
        var buttons = $('<div class="btn-group" ' +
                        'data-toggle="buttons"/>');

        panel_body.append(buttons);

        $.each(values, function (idx, value) {
            var button = $(
                '<a class="btn btn-default btn-xs active" role="button"/>');
            setup_callback(idx, value, button);
            buttons.append(button);
        });

        return panel_body;
    }

    function reflow_value_selector_panels(no_timeout) {
        $('.panel').each(function (i, panel_obj) {
            var panel = $(panel_obj);
            panel.find('.btn-group').each(function (i, buttons_obj) {
                var buttons = $(buttons_obj);
                var width = 0;

                if (buttons.hasClass('reflow-done')) {
                    /* already processed */
                    return;
                }

                $.each(buttons.children(), function(idx, value) {
                    width += value.scrollWidth;
                });

                var max_width = panel_obj.clientWidth;

                if (width >= max_width) {
                    buttons.addClass("btn-group-vertical");
                    buttons.css("width", "100%");
                    buttons.css("max-height", "20ex");
                    buttons.css("overflow-y", "auto");
                }
                else {
                    buttons.addClass("btn-group-justified");
                }

                /* The widths can be zero if the UI is not fully layouted yet,
                   so mark the adjustment complete only if this is not the case */
                if (width > 0 && max_width > 0) {
                    buttons.addClass("reflow-done");
                }
            });
        });

        if (!no_timeout) {
            /* Call again asynchronously, in case the UI was not fully layouted yet */
            setTimeout(function() { $.asv.ui.reflow_value_selector_panels(true); }, 0);
        }
    }

    function network_error(ajax, status, error) {
        $("#error-message").text(
            "Error fetching content. " +
            "Perhaps web server has gone down.");
        $("#error").modal('show');
    }

    function hover_graph(element, graph_url, benchmark_basename, parameter_idx, revisions) {
        /* Show the summary graph as a popup */
        var plot_div = $('<div/>');
        plot_div.css('width', '11.8em');
        plot_div.css('height', '7em');
        plot_div.css('border', '2px solid black');
        plot_div.css('background-color', 'white');

        function update_plot() {
            var markings = [];

            if (revisions) {
                $.each(revisions, function(i, revs) {
                    var rev_a = revs[0];
                    var rev_b = revs[1];

                    if (rev_a !== null) {
                        markings.push({ color: '#d00', lineWidth: 2, xaxis: { from: rev_a, to: rev_a }});
                        markings.push({ color: "rgba(255,0,0,0.1)", xaxis: { from: rev_a, to: rev_b }});
                    }
                    markings.push({ color: '#d00', lineWidth: 2, xaxis: { from: rev_b, to: rev_b }});
                });
            }

            $.asv.load_graph_data(
                graph_url
            ).done(function (data) {
                var params = $.asv.main_json.benchmarks[benchmark_basename].params;
                data = $.asv.filter_graph_data_idx(data, 0, parameter_idx, params);
                var options = {
                    colors: ['#000'],
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
                        minBorderMargin: 0,
                        markings: markings,
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
                var plot = $.plot(plot_div, [{data: data}], options);
            }).fail(function () {
                // TODO: Handle failure
            });

            return plot_div;
        }

        element.popover({
            placement: 'left auto',
            trigger: 'hover',
            html: true,
            delay: 50,
            content: $('<div/>').append(plot_div)
        });

        element.on('show.bs.popover', update_plot);
    }

    function hover_summary_graph(element, benchmark_basename) {
        /* Show the summary graph as a popup */
        var plot_div = $('<div/>');
        plot_div.css('width', '11.8em');
        plot_div.css('height', '7em');
        plot_div.css('border', '2px solid black');
        plot_div.css('background-color', 'white');

        function update_plot() {
            var markings = [];

            $.asv.load_graph_data(
                'graphs/summary/' + benchmark_basename + '.json'
            ).done(function (data) {
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
                        minBorderMargin: 0,
                        markings: markings,
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
                var plot = $.plot(plot_div, [{data: data}], options);
            }).fail(function () {
                // TODO: Handle failure
            });

            return plot_div;
        }

        element.popover({
            placement: 'left auto',
            trigger: 'hover',
            html: true,
            delay: 50,
            content: $('<div/>').append(plot_div)
        });

        element.on('show.bs.popover', update_plot);
    }

    /*
      Set up $.asv.ui
     */

    this.network_error = network_error;
    this.make_panel = make_panel;
    this.make_value_selector_panel = make_value_selector_panel;
    this.reflow_value_selector_panels = reflow_value_selector_panels;
    this.hover_graph = hover_graph;
    this.hover_summary_graph = hover_summary_graph;

    $.asv.ui = this;
});
