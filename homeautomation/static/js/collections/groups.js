  // js/collections/todos.js

  var app = app || {};

  // Todo Collection
  // ---------------

  // The collection of todos is backed by *localStorage* instead of a remote
  // server.
  app.GroupList = Backbone.Collection.extend({

    // Reference to this collection's model.
    model: app.Group,
    url: '/api/v0/groups'

  });

  // Create our global collection of **Todos**.
//  app.Groups = new GroupList();
