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

const topTracksIds = [
  '4bT9uDlsQjXP764yeQot7j','6uCqs7NlqHDAjdCUeUmgGI','5DT2fVrYGbXNhMYCnEFfg2','0AdD3U13ulNBHGhkdy6uVY','1ubY35d8LtYvMHsgPo8pMc'
];

async function getRecommendations(){
  // Endpoint reference : https://developer.spotify.com/documentation/web-api/reference/get-recommendations
  return (await fetchWebApi(
    `v1/recommendations?limit=5&seed_tracks=${topTracksIds.join(',')}`, 'GET'
  )).tracks;
}


async function GetRecommendations(){
    const recommendedTracks = await getRecommendations();
    console.log(
    recommendedTracks.map(
        ({name, artists}) =>
        `${name} by ${artists.map(artist => artist.name).join(', ')}`
    )
    );

  }
