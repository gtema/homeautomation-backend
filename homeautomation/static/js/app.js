var app = app || {};

$(function() {
    var books = [
        { name: 'JavaScript: The Good Parts'},
        { name: 'The Little Book on CoffeeScript'},
        { name: 'Scala for the Impatient'},
        { name: 'American Psycho'},
        { name: 'Eloquent JavaScript' }
    ];

    new app.GroupsView( books );
});
