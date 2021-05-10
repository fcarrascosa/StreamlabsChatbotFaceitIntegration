const parseSocketEventData = eventToParse => {
    const eventData = JSON.parse(eventToParse.data);
    const canBeReturned = typeof eventData.data === 'object' && eventData.data !== null || eventData.data === '';
    const { event } = eventData
    const data = canBeReturned
        ? eventData.data
        : JSON.parse(eventData.data);

    return { event, data }
}

const createSocketConnection = () => {
    const socket = new WebSocket(API_Socket);

    socket.onopen = () => {
        const auth = {
            author: "Fernando Carrascosa",
            website: "https://fcarrascosa.es",
            api_key: API_Key,
            events: [
                'EVENT_FCARRASCOSA_FACEIT_SESSION_START',
                'EVENT_FCARRASCOSA_FACEIT_SESSION_UPDATE'
            ]
        }

        socket.send(JSON.stringify(auth))
    }

    socket.onerror = error => {
        console.log(error)
        console.log("Connection Closed! Retrying...");
        createSocketConnection()
    }

    socket.onmessage = event => {
        const data = parseSocketEventData(event);
        console.log(Math.floor(Date.now() / 1000), data)
        switch (data.event) {
            case 'EVENT_FCARRASCOSA_FACEIT_SESSION_START':
                const idSelectors = [
                    'matchesPlayed',
                    'matchesWon',
                    'matchesLost',
                    'eloBalance'
                ];

                idSelectors.forEach(selector => {
                    document.getElementById(selector).querySelector('p.value').innerHTML = 0;
                });

                document.getElementById('eloBalance').classList.remove('lost', 'won');
                break;
            case 'EVENT_FCARRASCOSA_FACEIT_SESSION_UPDATE':
                const totalMatchesContainer = document.getElementById('matchesPlayed');
                const wonMatchesContainer = document.getElementById('matchesWon');
                const lostMatchesContainer = document.getElementById('matchesLost');
                const eloBalanceContainer = document.getElementById('eloBalance');

                totalMatchesContainer.querySelector('p.value').innerHTML = data.data.total_matches;
                wonMatchesContainer.querySelector('p.value').innerHTML = data.data.won_matches;
                lostMatchesContainer.querySelector('p.value').innerHTML = data.data.lost_matches;
                eloBalanceContainer.querySelector('p.value').innerHTML = data.data.elo_balance;

                if (data.data.elo_balance < 0) {
                    eloBalanceContainer.classList.add('lost')
                    eloBalanceContainer.classList.remove('won')
                } else if (data.data.elo_balance > 0) {
                    eloBalanceContainer.classList.remove('lost')
                    eloBalanceContainer.classList.add('won')
                } else {
                    eloBalanceContainer.classList.remove('lost', 'won')
                }
                break
            default:
                break;
        }
    }

    socket.onclose = () => {
        console.log("Connection Closed! Retrying...");
        createSocketConnection()
    }
}

createSocketConnection()
