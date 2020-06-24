#header_filter_by_lua_block {
#    ngx.header.content_length = nil
#}

local json_util = require("cjson")
local headers = ngx.header
local chunk, eof = ngx.arg[1], ngx.arg[2]

if ngx.ctx.buffered == nil then
    ngx.ctx.buffered = {}
end

if chunk ~= "" and not ngx.is_subrequest then
    table.insert(ngx.ctx.buffered, chunk)
    ngx.arg[1] = nil
end
if eof and ngx.status == 200 then
    if headers["Content-Type"] ~= nil and string.find(headers["Content-Type"], "application/json") ~= nil then
        local whole = table.concat(ngx.ctx.buffered)
        local d = json_util.decode(whole)
        if d.result ~= nil and d.result == "VAS-000" then
            d.result = "ORD-000"
        end
        ngx.arg[1] = json_util.encode(d)
    end
end
