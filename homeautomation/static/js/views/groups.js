var app = app || {};

app.GroupsView = Backbone.View.extend({
    el: '#appContent',

    initialize: function( initialData ) {
        this.collection = new app.GroupList( initialData );
        this.render();
    },

    // render library by rendering each book in its collection
    render: function() {
        this.collection.each(function( item ) {
            this.renderGroup( item );
        }, this );
    },

    // render a book by creating a BookView and appending the
    // element it renders to the library's element
    renderGroup: function( item ) {
        var groupView = new app.GroupView({
            model: item
        });
        this.$el.append( groupView.render().el );
    }
});
