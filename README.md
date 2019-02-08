# crypto-price-list
REST API service that returns actual cryptocurrency prices ordered by market capitalisation

## How to run

### 1. Clone repository

    $ git clone git@github.com:DominikZabron/crypto-price-list.git
    
### 2. Setup environment variables

Obligatory entries in `.env` file:

    COINMARKETCAP_KEY=xxxx
    CRYPTOCOMPARE_KEY=xxxx

### 3. Build docker images

    $ docker-compose build
    
### 4. Run microservices

    $ docker-compose up
    
## Usage

    $ curl http://localhost?limit=3
    [["BTC", 1, 3646.40839312], ["XRP", 2, 0.310457065183], ["ETH", 3, 118.478649517]]
    
## Rationale

Microservices use HTTP API for communication, that ensures easy-to-debug and maintenance of the services. However, different communication patterns were considered, especially regarding low-latency required when data would have to be updated more frequently. With the current state of the application, it assumes to fetch data from Cryptocompare and Coinmarketcap services using free API keys, and that would create possible bottleneck if more efficiency would be required from the application itself.
Special consideration should be given to multicast communication system if there is a plan to distribute the data from sources to multiple consumers. ZeroMQ would be a good choice for this design, allowing to address the same data to multiple destinations with only one call. I consider this approach have advantage over publish-subscribe model offered by AMQP protocol in this particular case.
Shared database is not advisable, as this model is dependent upon schema changes and requires complicated database migrations, however using database is handy for joining and ordering data. 
Application is built using API communication from producers to consumers with easy-to-write access, and reads are done by exploiting database view. For the more expensive join operations or high-traffic, might be worth to consider utilising for ex. triggers to transfer the data to another, physical table.
