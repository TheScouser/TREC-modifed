// Load all neccessary google charts packages
google.charts.load('current', {packages: ['line','bar','table','corechart']});  
// In order to avoid callback hell, we only draw anything after Google charts have loaded
google.charts.setOnLoadCallback(function(){
    // Get initialising data,populate the dropdowns and draw widgets
    getData();
    
    // Filter control
    $("#click").click(function(){
        if($("#click").hasClass('more')){
            $("#filters").slideDown(1000);
            $("#click").text("Less Filters");
            $("#click").addClass("less");
            $("#click").removeClass("more");
        }else{
            $("#filters").slideUp(1000);
            $("#click").text("More Filters");
            $("#click").addClass("more");
            $("#click").removeClass("less");
        }
    });

    // Get initialising data
    function getData() {
        $.ajax({
            url:'/get_init_data',
            type:'GET',
            datatype: 'json',
            success: function (data) {
                populateSideNav(data);
                getRuns(sanitiseParams());
            }
        });
    }
    // Get widgets parameters from widgets.json
    function getWidgets(data){
        $.ajax({
            url:'/get_widgets',
            type:'GET',
            datatype: 'json',
            success: function (widgets) {
                createChart(data,widgets);
            }
        });

    }

    // Get results for the chosen parameters
    // and create charts
    function getRuns(params){
        if (params != "") {
            $.ajax({
                url:'/get_results/'+params,
                type:'GET',
                datatype: 'json',
                success: function (data) {
                    getWidgets(data);
                }
            });
        }
        else{
            // If we reload the page we make sure it loads the same data
            var paramArray = window.location.pathname.split('/');
            getVariables = window.location.search;
            for (var i = 2; i < paramArray.length; i++) {
                params += "/"+paramArray[i];
            }
            $.ajax({
                url:'/get_results/'+params+getVariables,
                type:'GET',
                datatype: 'json',
                success: function (data) {
                    getWidgets(data);
                }
            });
        }  
    }

    // Creating the data tables that google charts require
    // in order to create the charts
	function createDataTable(data,tableType){
		var dataTable = new google.visualization.DataTable();
    	data = JSON.parse(data);

        // When logged in we have results page
        if (tableType == "semi"){
    	   dataTable.addColumn('string','Name');
    	   dataTable.addColumn('number','MAP');
    	   dataTable.addColumn('number','P10');
    	   dataTable.addColumn('number','P20');
    	   $.each(data, function(val){
    		  fields = data[val]["fields"];
    		  dataTable.addRow([fields["name"],fields["map"],fields["p10"],fields["p20"]]);
    	   });
        }
        // When logged out we have visitors page
        else if(tableType == "full"){
            dataTable.addColumn('string','Run Name');
            dataTable.addColumn('string', 'Description');
            dataTable.addColumn('string', 'Run Type');
            dataTable.addColumn('string', 'Researcher');
            dataTable.addColumn('string', 'Query Type');
            dataTable.addColumn('string', 'Feedback Type');
            dataTable.addColumn('number','MAP');
            dataTable.addColumn('number','P10');
            dataTable.addColumn('number','P20');
            $.each(data, function(val){
                fields = data[val]["fields"];
                if (fields["run_type"] == "0"){
                    run_type = "Automatic";
                }else{
                    run_type = "Manual";
                } 
                if(fields["query_type"] == "0"){
                    query_type = "Title";
                }else if(fields["query_type"] == "1"){
                    query_type = "Description";
                }else if(fields["query_type"]=="2"){
                    query_type = "Title and Description";
                }else if(fields["query_type"]=="3"){
                    query_type = "All";
                }else{
                    query_type = "Other";
                }
                if(fields["feedback_type"] == "0"){
                    feedback = "None";
                }else if(fields["feedback_type"] == "1"){
                    feedback = "Pseudo";
                }else if(fields["feedback_type"] == "2"){
                    feedback = "Relevance";
                }else{
                    feedback = "Other";
                }
                dataTable.addRow([fields["name"],fields["description"],run_type,fields["researcher"],query_type,feedback,fields["map"],fields["p10"],fields["p20"]]);
            });
        }
    	return dataTable;
	}
      

    // IF empty show an alert message
    // otherwise call drawChart with the widgets for the page
    function createChart(data,widgets){
        if(data.length == 2 ){
            $("#bar").html('<div class="callout alert"><h5>No results shown.</h5><p>There is no data for the selected options.</p></div>');
            $("#line").html('<div class="callout alert"><h5>No results shown.</h5><p>There is no data for the selected options.</p></div>');
            $("#table").html('<div class="callout alert"><h5>No results shown.</h5><p>There is no data for the selected options.</p></div>');
            return;
        }
        var type = window.location.pathname.split('/')[1];
        var widgetsArray = $.map(widgets, function(el) { return el });
        if (type == "Results") {   
            $.each(widgetsArray[0],function(val){
                var dataTable = createDataTable(data,widgetsArray[0][val]["type"]);
                drawChart(dataTable,val,widgetsArray[0][val]["options"]);
            });
        }
        else if(type == "Visitor"){
            $.each(widgetsArray[1],function(val){
                var dataTable = createDataTable(data,widgetsArray[1][val]["type"]);
                drawChart(dataTable,val,widgetsArray[1][val]["options"]);
            });
        }
    }

    // Used for building the params(and sanitising) for the query
    // and updating the url  
    function sanitiseParams(){
        var url = "";
        $('#submit').bind("click",function(){
            url=""
            track = $("#tracks option:selected").val();
            task = $("#tasks option:selected").val();
            run = $("#runs option:selected").val();
            keyword = $("#keyword").val();
            run_type = $("#run_types option:selected").val();
            query_type = $("#query_types option:selected").val();
            feedback_type = $("#feedback option:selected").val();
            researcher = $("#researchers option:selected").val();
            url+=track;
            if (task == "-") {
                task= "";
            }else{
                url += '/' + task;
            }
            if (run == "-" || run == undefined) {
                run= "";
            }else{
                url += '/' + run;
            }
            if (researcher == "-") {
                researcher = ""
            }
            if (run_type != "") {
                url += '?run_type=' + run_type;
            }
            if(query_type && run_type){
                url += '&query_type=' + query_type;
            }
            else if(query_type && !(run_type)){
                 url += '?query_type=' + query_type;
            }
            if(keyword && (run_type || query_type)){
                url += '&description=' +keyword;
            }else if(keyword && !(run_type || query_type)) {
                url += '?description=' +keyword;
            }
            if(feedback_type && (keyword || run_type || query_type)){
                url += '&feedback_type=' +feedback_type;
            }else if(feedback_type && !(keyword || run_type || query_type)) {
                url += '?feedback_type=' +feedback_type;
            }
            if(researcher && (feedback_type || keyword || run_type || query_type)){
                url += '&researcher=' +researcher;
            }else if(researcher && !(feedback_type || keyword || run_type || query_type)) {
                url += '?researcher=' +researcher;
            }
            pathname = window.location.pathname.split('/');
            history.replaceState(null,null,'/'+pathname[1]+'/'+url);
            getRuns(url);
        });
        return url;
    }
    });

// Draws a chart depending on the type and options
function drawChart(dataTable,type,options) {

    if (type == "line_chart"){
        var chart = new google.charts.Line(document.getElementById('line'));
        chart.draw(dataTable, options);
    }
    else if (type == "bar_chart") {
        var chart = new google.charts.Bar(document.getElementById('bar'));
        chart.draw(dataTable, options);
    }

    else if (type == "histogram_chart"){
        var chart = new google.visualization.Histogram(document.getElementById('histogram'));
        chart.draw(dataTable, options);
    }

    else if (type == "table_chart"){
        var chart = new google.visualization.Table(document.getElementById('table'));
        chart.draw(dataTable, options);
    }
}

// Populating the side navigation consisting of dropdown menus
function populateSideNav(data){
    var sideNav = $(".vertical.menu");
    tracks = JSON.parse(data["tracks"]);
    tasks = JSON.parse(data["tasks"]);
    runs = JSON.parse(data["runs"]);
    researchers = JSON.parse(data["researchers"]);
    // Populate researchers dropdown
    $.each(researchers, function(val){
        $("#researchers").append("<option value =\""+ researchers[val]["display_name"] +"\">"+ researchers[val]["display_name"] + "</option>");
    });
    var taskList = "<option value=\"-\" >-</option>";
    var runsList = "<option value=\"-\" >-</option>";
    // Populate tracks dropdown
    $.each(tracks, function(val){
        $("#tracks").append("<option value =\""+ tracks[val]["pk"]+"\">"+ tracks[val]["pk"] + "</option>");
    });
    // Populate tasks dropdown
    $.each(tasks, function(val){
        if($("#tracks option:selected").val() ==  tasks[val]["fields"]["track"]){
            $("#tasks").append("<option value =\""+ tasks[val]["pk"]+"\"> "+ tasks[val]["fields"]["title"] + " </option>");
        }
        $("#tasks").html(taskList);
    });
    // Event listener that will update tasks tasks when track has changed
    document.getElementById("tracks").addEventListener("change",function(){
        $.each(tasks, function(val){
            if($("#tracks option:selected").val() ==  tasks[val]["fields"]["track"]){
                taskList += "<option value =\""+ tasks[val]["pk"]+"\"> "+ tasks[val]["fields"]["title"]+" </option>";
            }
            if($("#tasks option:selected").val() ==  runs[val]["fields"]["task"]){
                runsList="<option value=\"-\" >-</option>";
                $("#runs").html(runsList);
            }
        });
        $("#tasks").html(taskList);
        taskList= "<option value=\"-\" >-</option>";
    });
    // Event listener that will update runs when task has changed
    document.getElementById("tasks").addEventListener("change",function(){
        runsList="<option value=\"-\" >-</option>";
        // Populate runs dropdown
        $.each(runs, function(val){
            if($("#tasks option:selected").val() ==  runs[val]["fields"]["task"]){
                runsList += "<option value = \"" + runs[val]["pk"]+"\">"+ runs[val]["fields"]["name"] + " </option>";
            }
        });
        $("#runs").html(runsList);
    });
}