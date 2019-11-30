# from riak import RiakClient, RiakNode
import riak

client = riak.RiakClient(protocol='http', host='172.19.0.2', http_port=8098)
client = riak.RiakClient(nodes=[
    {'host':'172.19.0.2','http_port':8098},
    {'host':'172.19.0.3','http_port':8098},
    {'host':'172.19.0.4','http_port':8098},
    {'host':'172.19.0.5','http_port':8098},
    {'host':'172.19.0.6','http_port':8098}
    ])
client = riak.RiakClient(protocol='http', nodes=[riak.RiakNode()])

# Choose the bucket to store data in.
bucket = client.bucket('test')

user_bucket = client.bucket('user')
profile_bucket = client.bucket('profile')
status_bucket = client.bucket('status')

# We're creating the user data & keying off their username.
new_user1 = user_bucket.new('johndoe', data={
    'first_name': 'John',
    'last_name': 'Doe',
    'gender': 'm',
    'website': 'http://example.com/',
    'is_active': True,
})
new_user2 = user_bucket.new('johndoe', data={
    'first_name': 'John Lenon',
    'last_name': 'Doe',
    'gender': 'm',
    'website': 'http://example.com/',
    'is_active': True,
})
# Note that the user hasn't been stored in Riak yet.
new_user1.store()
new_user2.store()

johndoe = user_bucket.get('johndoe')
new_profil = user_bucket.new('johndoe', data={
    'first_name': 'John',
    'last_name': 'Doe',
    'gender': 'm',
    'website': 'http://example.com/',
    'is_active': True,
})

profil = profile_bucket.get('a')


a = str(johndoe.data)
print(a)
print(profil.data)