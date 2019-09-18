import asyncio
import traceback

import aiofiles
import aiohttp
import aredis
from quart import Quart, request, current_app, jsonify

app = Quart(__name__)
app.redis_conn = aredis.StrictRedis("redis")


async def get_replicas(run_type):
    replicas_ = [replica.decode() for replica in (await app.redis_conn.hgetall("replicas")).keys()]
    result = []
    if run_type == 2:
        return replicas_
    for replica in replicas_:
        replica_status = await current_app.redis_conn.get(replica)
        if replica_status is None:
            replica_status = 0
        if int(replica_status) == run_type:
            result.append(replica)
    return result


@app.route("/replicas")
async def replicas():
    return jsonify(await get_replicas(int(request.args.get("type", "1"))))


@app.route("/refresh_ip/<replica_num>")
async def refresh_ip(replica_num):
    try:
        async with aiohttp.ClientSession() as session:
            await session.get(f"http://replica_{replica_num}:5000/reconnect")
        return ""
    except:
        return "error"


@app.route("/refresh_squid")
async def refresh_squid_api():
    await refresh_squid()
    return ""


async def refresh_squid():
    while 1:
        try:
            replicas_ = await get_replicas(run_type=1)
            _ = [f"cache_peer {replica} parent 3128 0 no-query\n" for replica in replicas_]
            async with aiofiles.open("/home/squid.conf.example", "r") as example_file:
                async with aiofiles.open("/etc/squid/squid.conf", "w") as output_file:
                    conf = await example_file.read()
                    await output_file.write(conf + f"\n\n{''.join(_)}")
            await asyncio.subprocess.create_subprocess_shell("squid -k reconfigure")
            break
        except:
            app.logger.error(traceback.format_exc())
            await asyncio.sleep(1)


if __name__ == '__main__':
    app.run("0.0.0.0")
