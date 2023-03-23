console.log("hello world");
//inner html is the content between tags
//value is only for input elements.
//var myFriends = ["Joe", "Steve", "John", "Sara"]

var mySongs = [];

var h1element = document.querySelector("h1");
console.log("my h1 element", h1element);

function makeInput(e) {
  var aClass = e.className + "edit";
  var userInput = e.innerText;
  e.innerHTML = '<input id="' + aClass + '" value="' + userInput + '">';
}

var addButton = document.querySelector("#add-song-button");
console.log("my button element", addButton);

function updateSong(
  songId,
  songName,
  songAlbum,
  songGenre,
  songArtist,
  songYear
) {
  console.log("attempting to update song", songName, "on server");

  var data = "&name=" + encodeURIComponent(songName);
  data += "&album=" + encodeURIComponent(songAlbum);
  data += "&genre=" + encodeURIComponent(songGenre);
  data += "&artist=" + encodeURIComponent(songArtist);
  data += "&year=" + encodeURIComponent(songYear);

  console.log("sending data to server:", data);

  fetch("http://localhost:8080/songs/" + songId, {
    //request details:
    method: "PUT",
    body: data,
    headers: {
      "Content-Type": "application/x-www-form-urlencoded",
    },
  }).then(function (response) {
    //when the server responds
    loadSongsFromServer();
  });
}

addButton.onclick = function () {
  console.log("my button was clicked");

  var songNameInput = document.querySelector("#song-name");
  console.log("my input element:", songNameInput);
  console.log("input element text:", songNameInput.value);

  var songAlbumInput = document.querySelector("#song-album");
  var songGenreInput = document.querySelector("#song-genre");
  var songArtistInput = document.querySelector("#song-artist");
  var songYearInput = document.querySelector("#song-year");

  //var mySongList = document.querySelector("#my-song-list");
  //console.log("my list element:", mySongList);

  //var newItem = document.createElement("li");
  //newItem.innerHTML = songNameInput.value; //makes value appear in list

  //mySongList.appendChild(newItem);
  //console.log("item added to myList");

  createSongOnServer(
    songNameInput.value,
    songAlbumInput.value,
    songGenreInput.value,
    songArtistInput.value,
    songYearInput.value
  );
  //clears what they typed
  songNameInput.value = "";
  songAlbumInput.value = "";
  songGenreInput.value = "";
  songArtistInput.value = "";
  songYearInput.value = "";
};

function loadSongsFromServer() {
  fetch("http://localhost:8080/songs").then(function (response) {
    response.json().then(function (data) {
      console.log("data received from server.", data);
      mySongs = data; // or myFriends = data.record;

      var myList = document.querySelector("#my-song-list");
      console.log("my list element:", myList);
      myList.innerHTML = "";

      mySongs.forEach(function (song) {
        var newSong = document.createElement("li");
        var nameDiv = document.createElement("div");
        nameDiv.innerHTML = song.name; //work on this part
        nameDiv.classList.add("song-name");
        newSong.appendChild(nameDiv);

        var albumDiv = document.createElement("div");
        albumDiv.innerHTML = song.album; //work on this part
        albumDiv.classList.add("song-album");
        newSong.appendChild(albumDiv);

        var genreDiv = document.createElement("div");
        genreDiv.innerHTML = song.genre; //work on this part
        genreDiv.classList.add("song-genre");
        newSong.appendChild(genreDiv);

        var artistDiv = document.createElement("div");
        artistDiv.innerHTML = song.artist; //work on this part
        artistDiv.classList.add("song-artist");
        newSong.appendChild(artistDiv);

        var yearDiv = document.createElement("div");
        yearDiv.innerHTML = song.year; //work on this part
        yearDiv.classList.add("song-year");
        newSong.appendChild(yearDiv);

        myList.appendChild(newSong);

        var deleteButton = document.createElement("button");
        deleteButton.innerHTML = "Delete";
        deleteButton.className = "delete-button";
        deleteButton.onclick = function () {
          console.log("delete button was clicked for ", song.name);
          if (confirm("Are you sure you want to delete " + song.name + "?")) {
            deleteSongFromServer(song.id);
          }
        };
        newSong.appendChild(deleteButton);

        var editButton = document.createElement("button");
        editButton.innerHTML = "Edit";
        editButton.className = "edit_button";

        editButton.addEventListener(
          "click",
          function () {
            console.log("edit button was clicked for ", song.name);
            var save_button = document.createElement("button");
            newSong.appendChild(save_button);
            save_button.innerHTML = "Save";
            makeInput(nameDiv);
            makeInput(albumDiv);
            makeInput(genreDiv);
            makeInput(artistDiv);
            makeInput(yearDiv);

            save_button.onclick = function () {
              var name = document.querySelector("#song-nameedit");
              var album = document.querySelector("#song-albumedit");
              var genre = document.querySelector("#song-genreedit");
              var artist = document.querySelector("#song-artistedit");
              var year = document.querySelector("#song-yearedit");
              updateSong(
                song.id,
                name.value,
                album.value,
                genre.value,
                artist.value,
                year.value
              );
            };
          },
          { once: true }
        );

        newSong.appendChild(editButton);

        myList.appendChild(newSong);
      });
    });
  });
}

function createSongOnServer(
  songName,
  songAlbum,
  songGenre,
  songArtist,
  songYear
) {
  console.log("attempting to create song", songName, "on server");

  var data = "name=" + encodeURIComponent(songName);
  data += "&album=" + encodeURIComponent(songAlbum);
  data += "&genre=" + encodeURIComponent(songGenre);
  data += "&artist=" + encodeURIComponent(songArtist);
  data += "&year=" + encodeURIComponent(songYear);

  console.log("sending data to server:", data);

  fetch("http://localhost:8080/songs", {
    //request details:
    method: "POST",
    body: data,
    headers: {
      "Content-Type": "application/x-www-form-urlencoded",
    },
  }).then(function (response) {
    //when the server responds
    if (response.status == 201) {
      loadSongsFromServer();
    } else {
      console.log(
        "server respoded with",
        response.status,
        "when trying to create a song"
      );
    }
  });
}

function deleteSongFromServer(songId) {
  fetch("http://localhost:8080/songs/" + songId, {
    method: "DELETE",
  }).then(function (response) {
    console.log(response);
    if (response.status == 204) {
      loadSongsFromServer();
    } else {
      console.log(
        "server responded with",
        response.status,
        "when trying to delete a song"
      );
    }
  });
}

function updateSongFromServer(
  memberId,
  songName,
  songAlbum,
  songGenre,
  songArtist,
  songYear
) {
  console.log("attempting to update song", songName, "on server");

  var data = "name=" + encodeURIComponent(songName);
  data += "&album=" + encodeURIComponent(songAlbum);
  data += "&genre=" + encodeURIComponent(songGenre);
  data += "&artist=" + encodeURIComponent(songArtist);
  data += "&year=" + encodeURIComponent(songYear);

  console.log("sending data to server:", data);

  fetch("http://localhost:8080/songs" + "/" + memberId, {
    //request details:
    method: "PUT",
    body: data,
    headers: {
      "Content-Type": "application/x-www-form-urlencoded",
    },
  }).then(function (response) {
    //when the server responds
    if (response.status == 201) {
      loadSongsFromServer();
    } else {
      console.log(
        "server respoded with",
        response.status,
        "when trying to create a song"
      );
    }
  });
}

loadSongsFromServer();
