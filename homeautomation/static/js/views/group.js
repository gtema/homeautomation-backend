
var app = app || {};

app.GroupView = Backbone.View.extend({
    tagName: 'li',
    className: 'groupContainer',
    template: _.template( $( '#groupTemplate' ).html() ),

    render: function() {
        //this.el is what we defined in tagName. use $el to get access to jQuery html() function
        this.$el.html( this.template( this.model.attributes ) );

        return this;
    }
});
