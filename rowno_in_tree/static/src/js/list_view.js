odoo.define('rowno_in_tree.ListNumber', function (require) {
"use strict";

var core = require('web.core');
var ListRenderer = require('web.ListRenderer');
var _t = core._t;

console.log(core,"corecorecorecore")
console.log(ListRenderer,"ListRendererListRendererListRenderer")

ListRenderer.include({
	_getNumberOfCols: function () {
		var columns = this._super();
		columns +=1;
		return columns;
    },
    _renderFooter: function (isGrouped) {
    	var $footer = this._super(isGrouped);
    	$footer.find("tr").prepend($('<td>'));
    	return $footer;
    },
    _renderGroupRow: function (group, groupLevel) {
        var $row =  this._super(group, groupLevel);
        if (this.mode !== 'edit' || this.hasSelectors){
        	$row.find("th.o_group_name").after($('<td>'));
        }
        return $row;
    },
    _renderGroups: function (data, groupLevel) {
    	var self = this;
    	var _self = this;
        groupLevel = groupLevel || 0;
        var result = [];
        var $tbody = $('<tbody>');
        _.each(data, function (group) {
            if (!$tbody) {
                $tbody = $('<tbody>');
            }
            $tbody.append(self._renderGroupRow(group, groupLevel));
            if (group.data.length) {
                result.push($tbody);
                if (group.groupedBy.length) {
                    result = result.concat(self._renderGroups(group.data, groupLevel + 1));
                } else {
                    var $records = _.map(group.data, function (record,index) {
                    	if (_self.mode !== 'edit' || _self.hasSelectors){
                    		return self._renderRow(record).prepend($('<th>').html(index+1)).prepend($('<td>'));
                    	}
                    	else{
                    		return self._renderRow(record).prepend($('<td>'));
                    	}
                    	
                    });
                    result.push($('<tbody>').append($records));
                }
                $tbody = null;
            }
        });
        if ($tbody) {
            result.push($tbody);
        }
        return result;
    },
    _renderHeader: function (isGrouped) {
    	var $header = this._super(isGrouped);
    	if (this.hasSelectors) {
    		$header.find("th.o_list_record_selector").before($('<th class="o_list_row_number_header">').html('#'));
    		var advance_search = $header.find("tr.advance_search_row")
    		if(advance_search.length && advance_search.find('td.o_list_row_number_header').length==0){    			
    			advance_search.prepend($('<td class="o_list_row_number_header">').html('&nbsp;'));
    		}
        }
    	else{
    		if (this.mode !== 'edit'){
    			$header.find("tr").prepend($('<th>').html('#'));
    		}
    	}
    	return $header;
    },
    _renderRow: function (record) {
    	var $row = this._super(record);
    	if (this.mode !== 'edit' && this.state.groupedBy.length==0){
	    	var index = this.state.data.findIndex(function(e){return record.id===e.id})
	    	if (index!==-1){
	    		$row.prepend($('<th>').html(index+1));
	    	}
    	}
    	return $row;
    	
    },
    
}); 

});

