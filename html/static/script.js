function delete_object(db, id, rev) {
    let data = {"prepid": id, "_rev": rev};
    $.ajax({
       type: "DELETE",
       contentType: "application/json",
       url: "/api/" + db + "/delete",
       data: JSON.stringify(data),
     }).done(function (data) {
     console.log(data);
     }).fail(function(data) {
    console.log(data);
})
}

function add_object(db,id,rev) {
    let data = {"prepid": id, "_rev": rev};
    $.ajax({
    type: "ADD",
    contentType: "application/json",
    url: "/api/" + db + "/add",
    data: JSON.stringify(data),
   }).done(function (data) {
    console.log(data);
  }).fail(function(data) {
 console.log(data);
})
}

function modify_object(db,id,rev) {
    let data = {"prepid": id, "_rev": rev};
    $.ajax({
    type: "MODIFY",
    contentType: "application/json",
    url: "/api/" + db + "/modify",
    data: JSON.stringify(data),
   }).done(function (data) {
    console.log(data);
  }).fail(function(data) {
 console.log(data);
})
}

