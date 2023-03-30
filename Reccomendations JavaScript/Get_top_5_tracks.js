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

async function getTopTracks(){
  // Endpoint reference : https://developer.spotify.com/documentation/web-api/reference/get-users-top-artists-and-tracks
  return (await fetchWebApi(
    'v1/me/top/tracks?time_range=short_term&limit=5', 'GET'
  )).items;
}

async function GetNames(){
    const topTracks = await getTopTracks();
    console.log(
    topTracks?.map(
        ({name, artists}) =>
        `${name} by ${artists.map(artist => artist.name).join(', ')}`
    )
    );
    console.print(topTracks);
    
    
}
