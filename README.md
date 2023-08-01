# UP4W-PY

`up4w` is a collection of python libraries written in Python 3, with built-in type declaration files. It is used for interacting with the [UP4W](https://github.com/up4w/up4w-core/blob/master/docs/index.md) JSON API 

- Python 3.8+ support

## Installation

```
pip install up4w
```

## Data response structure

All interfaces are implemented to return a standard json-object. The data structure returned is as follows:

| Field | Type | Description | Required |
|----|----|----|---|
| rsp | string | The module action |Y|
| ret | object | The data returned has a specific structure that can vary depending on the interface. | N |
| fin | boolean | indicates whether more messages will be responded |N|
| err | number | Error reason, returned only when an error occurs. | N |

> More infomation about response structure [UEP_0021](https://github.com/up4w/up4w-core/blob/master/docs/uep_0021.md)

Here is a example:

```
{
  rsp: "msg.received",
  ret: {
    id: "3866091278",
    timestamp: 1684658460224,
    app: 1,
    action: 4096,
    "recipient": "<a_base64_encode_address>"
    sender: ":myself",
    content: "Explain quantum computing in simple terms",
    content_type: 13,
  },
}
```

## Usage example

A basic example:

```
import asyncio
import time
from up4w import UP4W


async def main():
    up4w = UP4W()

    # Get UP4W Version
    version = up4w.get_ver()
    # Output {'rsp': 'core.ver', 'ret': 'version 1.1, build Jul 5 2023 16:25:55'}
    print(version)

    # Continuously receive message pushed by UP4W
    def get_message_pushed(t):
        print("get_message_pushed", t)

    up4w.message.receive_message(get_message_pushed)

    # Do what you want by using 'up4w' instance
    up4w.wait_for_initialize({
        app_name: "deso",
        mrc: {
          msgs_dir: ":mem",
          default_swarm: "<a_base64_address>", //replace it with your swarm address
          flags: ["delay00_load"],
        },
        mlt: {},
        gdp: {},
        pbc: {},
        lsm: {},
    })

if __name__ == "__main__":
    asyncio.run(main())
    time.sleep(15)
```

## up4w

A collection of methods for interacting with the underlying UP4W network.

```
from up4w import UP4W
up4w = UP4W()
```

### Returns

A instance of `up4w` instance

### Exmaple

#### up4w.get_ver()

Get version and build information of the peer, no arguments.

```
version = up4w.get_ver()
// output:{  rsp: 'core.ver', inc: '41c870e4389fceab', ret: 'version 1.1, build May 20 2023 20:45:33' }
print(version)
```

##### Parameters

none

##### Returns

a version string

#### up4w.wait_for_initialize(params)

Initialize all desired modules.

```
result = up4w.wait_for_initialize({
  app_name: 'deso',
  mrc: {
    msgs_dir: ':mem',
   default_swarm: "<a_base64_address>",
    flags: ['delay00_load'],
  },
  mlt: {},
  gdp: {},
  pbc: {},
  lsm: {},
})
print(result) // output: True
```

##### Parameters:

##### `params` - `object`

- `app_name` is the name of the application, instances with different `app_name` will not discover each other in nearby peers ([UEP-8](https://github.com/up4w/up4w-core/blob/master/docs/uep_0008.md))
- `mrc` initialize message relay core ([UEP-12](https://github.com/up4w/up4w-core/blob/master/docs/uep_0012.md)), `msgs_dir` specifies the storage directory for saving pooled messages, or its value can be `:mem` to just memory for temporary storage.
- `media_dir` specifies storage directory for saving offload media, if specified, the distributed media store [(UEP-16](https://github.com/up4w/up4w-core/blob/master/docs/uep_0016.md)) will be initialized as well.
- `dvs` initialize distributed key-value store ([UEP-20](https://github.com/up4w/up4w-core/blob/master/docs/uep_0020.md)) with `kv_dir` specifies the storage directory, or memory.
- flags
  - "delay_load" indicates the `media` db or the `kv` db is not loaded when initialization
  - "db_dedicate" two db on disk, one for default swarm, another for all non-default ones (merged)
  - "db_separated" one separated db on disk for every swarm
  - "db_merged" a single db for all swarms (merged)
- `hob` enable packet obfuscation ([UEP-6](https://github.com/up4w/up4w-core/blob/master/docs/uep_0006.md)).
- `lsm` initialize nearby peers module ([UEP-8](https://github.com/up4w/up4w-core/blob/master/docs/uep_0008.md)).
- `mlt` enable multi-link tunnels
- `gdp` initialize gossip data protocol ([UEP-11](https://github.com/up4w/up4w-core/blob/master/docs/uep_0011.md)), it will be automatically initialized if `mrc` or `dvs` is specified.
- `pbc` enable packet bouncer

#### Returns

 `bool`. True means initialize succesfully, otherwise failed.

#### up4w.shutdown()

Uninitialize the `UP4W` stacks, no arguments, no return. Shutdown is unrecoverable.

```
up4w.shutdown()
```

##### Parameters

`None`

##### Returns

`None`

### up4w.social

#### up4w.social.signin_with_seed(seed, *，name: str = None, gender: int = None,geolocation: int = None, greeting_secret: str = None)

Set current sign-in user by seed(private key)

```
result = up4w.social.signin_with_seed("<a_base64_seed_string>")
// output '{"rsp":"social.signin","inc":"51db8a36ac7ef161","ret":{"pk":"e6t9rv1...pkgen3y40v73z0"}}'
print(user)
```

##### Parameters

`seed` is the 28-byte root seed 

##### Returns

`object` 

- pk - `string` a public key that has been encoded using `Base64`

#### up4w.social.signin_with_mnemonic(words, *，name: str = None, gender: int = None, geolocation: int = None, greeting_secret: str = None)

Set current sign-in user by mnemonic words, this function is equivalent to `up4w.siginWithSeed`, but the difference lies in the input parameter.

```
result = up4w.social.signin_with_mnemonic("migrant adipex ... laos since")
// output '{"rsp":"social.signin","inc":"51db8a36ac7ef161","ret":{"pk":"e6t9rv1...pkgen3y40v73z0"}}'
print(user)
```

##### Parameters

- words - `string` A list of 18 mnemonic words separated by spaces.
- name - `str` `optional`
- gender - `int` `optional`
- geolocation - `int` `optional`
- greeting_secret - `int` `optional`

##### Returns

Same to `up4w.siginWithSeed`

#### up4w.social.add_user( pk: str, *, name: str = None, gender: int = None, geolocation: int = None, greeting_secret: str = None)

Add a new user in the contact list, no return. This method will not send a greeting message to the user.

```
result = up4w.social.add_user("Target_User_PK", name="Lufy", gender=3)
// output {"rsp":"social.add_user","inc":"43bbe30cc17b88c6","ret":null}
print(result)
```

##### Parameters

user - `object`

- pk`string` a public key that has been encoded using `Base64`
- name `string` User's name , optional
- gender `string` User's gender, optional
- geolocation`string` User's geographical location, optional
- greeting_secret `string`is the greeting secret required for adding a new friend, optional

##### Returns

`object`

#### up4w.social.remove_user(pk)

Remove an existing user, no return.

```
result = up4w.social.remove_user(Target_User_PK)
// output {"rsp":"social.remove_user","inc":"43bbe30cc17b88c6","ret":null}
print(result)
```

##### Parameters

- pk`string` a public key that has been encoded using `Base64`

##### Returns

`object`

## up4w.message

> See [Core Social Messaging APIs](https://github.com/up4w/up4w-core/blob/master/docs/uep_0022.md)

#### up4w.message.receive_message(callback)

Subscribe to message push notifications to listen for all events pushed by the `UP4W` network, such as chat replies, and so on.

```
from up4w import UP4W
def main():
    up4w = UP4W()
    
    # Continuously receive message pushed by UP4W
    def get_message_pushed(message):
        print("get_message_pushed", message)
        
    up4w.message.receive_message(get_message_pushed)

if __name__ == "__main__":
    main()
    time.sleep(15)

```

The `message` looks like:

```
{
    "rsp": "msg.received",
    "ret": {
    	"swarm": " ... ",
        "id": "795100302",
        "timestamp": 1684752857888,
        "app": 1,
        "action": 4097,
        "recipient": "<a_base64_encode_address>",
        "sender": "<a_base64_encode_address>",
        "content": "Quantum computing is a type of computing that ...",
        "content_type": 13
    }
}
```

##### Parameters

- callback: `function(message)`

  - swram - `string` the swarm DHT address in base16, or the alias as set by join swarm request (`req:"swarm.join"`, [UEP-21](https://github.com/up4w/up4w-core/blob/master/docs/uep_0021.md))
  - `id` the id of the message in the scope of current swarm, a `uint64_t` in string.
  - timestamp - `number` of the message in millisecond
  - sender -`string`: the public key of the sender in base64
  - app -`number` the built-in application id, an `uint16_t`
  - action -`number` the operation code specific to the application, an `uint16_t`
  - recipient - `string` stands for the recipient, which is a user's `pubkey` or that of a scenario-specific identity ([UEP-13](https://github.com/up4w/up4w-core/blob/master/docs/uep_0013.md))
  - content -`string` the content of the message can be parsed object, a plain text, or a base64 string according to `app` and `action`
  - content_type -`number` the type of the content ([UEP-17](https://github.com/up4w/up4w-core/blob/master/docs/uep_0017.md))
  - media -`array` attached media blobs . Note that, a pair of `<timestamp, crc>` is used to uniquely identify a message.

- receiveParams - `object`
  - conversation - `string` a `base64` encoded public key, optional
  - app - `number` application id, optional

##### Returns

none

#### up4w.message.sendText(message)

Send a text message to a specific recipient.

```
#...
up4w = up4w()

# Continuously receive message pushed by UP4W
def get_message_pushed(t):
	print("get_message_pushed", t)
up4w.message.receive_message(get_message_pushed)

# Do what you want by using 'up4w' instance
up4w.wait_for_initialize({
    app_name: "deso",
    mrc: {
        msgs_dir: ":mem",
        default_swarm: "<a_base64_address>", //replace it with your swarm address
        flags: ["delay00_load"],
    },
    mlt: {},
    gdp: {},
    pbc: {},
    lsm: {},
})
up4w.social.add_user(<a_base64_encode_publickey>, name="Lufi")

result = up4w.message.send_text({
    "recipient": "<a_base64_encode_address>",
    "app": 1,
    "action": 4096,
    "content": "Explain quantum computing in simple terms",
})
print(result)
```

result:

```
{
    "rsp": "msg.text",
    "inc": "be30cc17b88c6c76",
    "ret": {
        "swarm": "<your_swarm_address>",
        "id": "1816980011727310231",
        "timestamp": 1684752850240
    }
}
```

##### Parameters

- swarm - `string` the swarm DHT address in `base16` ,optional
- recipient - `string` stands for the recipient, which is a user's `pubkey` or that of a scenario-specific identity
- app - `number`application_id
- action - `number` operation code
- content - `string` `object` message content
- content_type - `number` content type, text message always be `13`, optional

##### Returns

`object`

- swarm - `string` the swarm DHT address
- id - `string` id of message
- timestamp - `number` Sending time for millisecond

## up4w.swarm

### up4w.swarm.join(node)

Join a swarm and initialize swarm-specific protocols, no return.

```
up4w.swarm.join(node)
```

##### Parameters

node - `object`

- `address` the 20-byte DHT address of the swarm in base16
- `secret` the 32-byte private swarm secret in base64, optional. If specified, the swarm will be private swarm
- `epoch` the epoch unit in millisecond for the DAGM ([UEP-12](https://github.com/up4w/up4w-core/blob/master/docs/uep_0012.md))
- `ttl` the max TTL in epoch for the DAGM
- `subband` the range of the subband, should be 2^n.
- `media_sizemax` the maximum size of attached media in messages, unspecified or 0 indicates media attachment is not allowed
- `active` inbound message will be pushed as a (`rsp:"msg_received"`) message ([UEP-22](https://github.com/up4w/up4w-core/blob/master/docs/uep_0022.md)) if decryption succeeded
- `value_sizemax` the maximum size of values in DVS ([UEP-20](https://github.com/up4w/up4w-core/blob/master/docs/uep_0020.md))

##### Returns

`Object `

### up4w.swarm.leave(address)

Leave a swarm

```
up4w.swarm.leave(address)
```

##### Parameters

- `address` the 20-byte DHT address of the swarm in base16

##### Returns

`Object `

## up4w.persistence

Distributed Key-Value Storage

#### up4w.persistence.set(data)

Set a value .

```
result = up4w.persistence.set(data)
// output {"rsp":"netkv.set","inc":"43bbe30cc17b88c6","ret":null}
print(result)
```

##### Parameters

data- `object`

- `key` the 32-byte datakey in base 64 ([UEP-21](https://github.com/up4w/up4w-core/blob/master/docs/uep_0021.md))
- `slot` the storage slot of the value (0~255)
- `ttl` the TTL in seconds of the value
- `value` the value data in base64
- `secret` the AES secret for value encryption, optional.

##### Returns

`Object` with null `ret`

#### up4w.persistence.get(data)

Get a value.

```
result = up4w.persistence.get(data)
// output {"rsp":"netkv.get","inc":"43bbe30cc17b88c6","ret":null}
print(result)
```

##### Parameters

data- `object`

- `key` the 32-byte datakey in base 64([UEP-20](https://github.com/up4w/up4w-core/blob/master/docs/uep_0020.md))
- `slot` the storage slot of the value (0~255)
- `secret` the secret for value encryption, optional.
- `raw` indicate the response to be the raw binary media data, optional and synchronous invocation only

##### Returns

`Object` , whose `ret` with vary result:

- if the value is not encrypted, or correct secret is provided, a `base64` encoded string will be return;

- if `raw` is true, the response is just the raw binary data without the json formatted response encapsulation.
