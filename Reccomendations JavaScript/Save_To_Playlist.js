// Authorization token that must have been created previously. See : https://developer.spotify.com/documentation/web-api/concepts/authorization
const token = 'BQBeDPk5YmSHocp5QU3WX-tdo7boKbubqVjYjjdO6ICkxnypOycNs-H0w9mymXJlbmM7a0MVkfxilCY6vYnKv7t7KpPy2yuZcb5AAgNiHR8Wx3GyyuzwnudKjxPZSgd2spWyhtiIHzqO--qfHn8JfL3ahyYgEW1cx6Qaa847KqnCsSgyKGQFrhVWU62OkWw-g5tqz4P63fZAlITTtsDl1aEjplMPW5awRos0o3gXfJf8arGOacudGrGmZ-RHr9WFDISTQ6jPpkOzbytsgeLl7gNe40HLAvEu6skwxdzy538PxDYhXpRmWpOsd_9HDx1IGeu0JrMxYePi2Qcsr7ZtNlKor82XqGrNBve7XjFqVoBsEGU';
async function fetchWebApi(endpoint, method, body) {
  const res = await fetch(`https://api.spotify.com/${endpoint}`, {
    headers: {
      Authorization: `Bearer ${token}`,
    },
    method,
    body:JSON.stringify(body)
  });
  return await res.json();
}

const tracksUri = [
  'spotify:track:4bT9uDlsQjXP764yeQot7j','spotify:track:6DEA5Mzz2HxvhM7Nfdi0Dp','spotify:track:6uCqs7NlqHDAjdCUeUmgGI','spotify:track:6BIeZ7d6uUzRHqBPBMxTDD','spotify:track:5DT2fVrYGbXNhMYCnEFfg2','spotify:track:2slMNyaT0nrXneGLktdhiW','spotify:track:0AdD3U13ulNBHGhkdy6uVY','spotify:track:6gqz1UrYCkdpcQCAHgMM0m','spotify:track:1ubY35d8LtYvMHsgPo8pMc','spotify:track:2mHZigVkpJ1GcUQI554biS'
];
const user_id = '7gau3mfurpamvofd00ej790p9';

async function createPlaylist(tracksUri){
  return await fetchWebApi(
    `v1/users/${user_id}/playlists`, 'POST', {
      "name": "My recommendation playlist",
      "description": "Playlist created by the tutorial on developer.spotify.com",
      "public": false
  }).then(playlist => {
    fetchWebApi(
      `v1/playlists/${playlist.id}/tracks?uris=${tracksUri.join(',')}`,
      'POST'
    );
    return playlist;
  })
}

async function CreatePlaylist(){
    const createdPlaylist = await createPlaylist(tracksUri);
    console.log(createdPlaylist.name, createdPlaylist.id);
}
