# gfw-proxy-domain

合并多个开源规则库的国外代理（GFW / Proxy）域名，去掉前缀、正则、关键词和 IP 类规则，统一小写、校验格式后去重，并剔除与国内直连列表完全相同的域名，输出一行一个的纯域名。每天北京时间 02:45 由 GitHub Actions 自动更新。

最近更新：2026-10-26 03:10 CST　上游来源：33 个（成功 33，失败 0）

## 文件

| 文件 | 说明 | 条数 | 链接 |
| --- | --- | ---: | --- |
| gfw-proxy-domains.txt | 精简版（父域名已在列表时去掉子域名） | 48,581 | [raw](https://raw.githubusercontent.com/passionsu-su/gfw-proxy-domain/main/gfw-proxy-domains.txt) |
| gfw-proxy-domains-full.txt | 完整去重版 | 58,232 | [raw](https://raw.githubusercontent.com/passionsu-su/gfw-proxy-domain/main/gfw-proxy-domains-full.txt) |
| stats.json | 各来源条数与失败来源 | - | [raw](https://raw.githubusercontent.com/passionsu-su/gfw-proxy-domain/main/stats.json) |

## 上游规则库

| # | 来源 | 规则库 | 文件 | 有效域名数 | 状态 |
| ---: | --- | --- | --- | ---: | --- |
| 1 | Loyalsoldier proxy-list | [Loyalsoldier/v2ray-rules-dat](https://github.com/Loyalsoldier/v2ray-rules-dat) | [proxy-list.txt](https://github.com/Loyalsoldier/v2ray-rules-dat/blob/release/proxy-list.txt) | 27,246 | 正常 |
| 2 | Loyalsoldier gfw | [Loyalsoldier/v2ray-rules-dat](https://github.com/Loyalsoldier/v2ray-rules-dat) | [gfw.txt](https://github.com/Loyalsoldier/v2ray-rules-dat/blob/release/gfw.txt) | 4,443 | 正常 |
| 3 | Loyalsoldier clash-rules proxy | [Loyalsoldier/clash-rules](https://github.com/Loyalsoldier/clash-rules) | [proxy.txt](https://github.com/Loyalsoldier/clash-rules/blob/release/proxy.txt) | 27,246 | 正常 |
| 4 | Loyalsoldier clash-rules gfw | [Loyalsoldier/clash-rules](https://github.com/Loyalsoldier/clash-rules) | [gfw.txt](https://github.com/Loyalsoldier/clash-rules/blob/release/gfw.txt) | 4,443 | 正常 |
| 5 | gfwlist | [gfwlist/gfwlist](https://github.com/gfwlist/gfwlist) | [gfwlist.txt](https://github.com/gfwlist/gfwlist/blob/master/gfwlist.txt) | 4,374 | 正常 |
| 6 | blackmatrix7 Global_Domain | [blackmatrix7/ios_rule_script](https://github.com/blackmatrix7/ios_rule_script) | [Global_Domain.list](https://github.com/blackmatrix7/ios_rule_script/blob/master/rule/Shadowrocket/Global/Global_Domain.list) | 35,101 | 正常 |
| 7 | blackmatrix7 Proxy_Domain | [blackmatrix7/ios_rule_script](https://github.com/blackmatrix7/ios_rule_script) | [Proxy_Domain.list](https://github.com/blackmatrix7/ios_rule_script/blob/master/rule/Shadowrocket/Proxy/Proxy_Domain.list) | 6,839 | 正常 |
| 8 | ACL4SSR ProxyGFWlist | [ACL4SSR/ACL4SSR](https://github.com/ACL4SSR/ACL4SSR) | [ProxyGFWlist.list](https://github.com/ACL4SSR/ACL4SSR/blob/master/Clash/ProxyGFWlist.list) | 6,867 | 正常 |
| 9 | ACL4SSR ProxyLite | [ACL4SSR/ACL4SSR](https://github.com/ACL4SSR/ACL4SSR) | [ProxyLite.list](https://github.com/ACL4SSR/ACL4SSR/blob/master/Clash/ProxyLite.list) | 313 | 正常 |
| 10 | Johnshall sr_top500_banlist | [Johnshall/Shadowrocket-ADBlock-Rules-Forever](https://github.com/Johnshall/Shadowrocket-ADBlock-Rules-Forever) | [sr_top500_banlist.conf](https://github.com/Johnshall/Shadowrocket-ADBlock-Rules-Forever/blob/release/sr_top500_banlist.conf) | 30,209 | 正常 |
| 11 | LOWERTOP RULE-SET AI.txt | [iab0x00/ProxyRules](https://github.com/iab0x00/ProxyRules) | [AI.txt](https://github.com/iab0x00/ProxyRules/blob/main/Rule/AI.txt) | 62 | 正常 |
| 12 | LOWERTOP RULE-SET YouTube.list | [blackmatrix7/ios_rule_script](https://github.com/blackmatrix7/ios_rule_script) | [YouTube.list](https://github.com/blackmatrix7/ios_rule_script/blob/master/rule/Shadowrocket/YouTube/YouTube.list) | 178 | 正常 |
| 13 | LOWERTOP RULE-SET Netflix.list | [blackmatrix7/ios_rule_script](https://github.com/blackmatrix7/ios_rule_script) | [Netflix.list](https://github.com/blackmatrix7/ios_rule_script/blob/master/rule/Shadowrocket/Netflix/Netflix.list) | 33 | 正常 |
| 14 | LOWERTOP RULE-SET Disney.list | [blackmatrix7/ios_rule_script](https://github.com/blackmatrix7/ios_rule_script) | [Disney.list](https://github.com/blackmatrix7/ios_rule_script/blob/master/rule/Shadowrocket/Disney/Disney.list) | 172 | 正常 |
| 15 | LOWERTOP RULE-SET HBO.list | [blackmatrix7/ios_rule_script](https://github.com/blackmatrix7/ios_rule_script) | [HBO.list](https://github.com/blackmatrix7/ios_rule_script/blob/master/rule/Shadowrocket/HBO/HBO.list) | 47 | 正常 |
| 16 | LOWERTOP RULE-SET Spotify.list | [blackmatrix7/ios_rule_script](https://github.com/blackmatrix7/ios_rule_script) | [Spotify.list](https://github.com/blackmatrix7/ios_rule_script/blob/master/rule/Shadowrocket/Spotify/Spotify.list) | 26 | 正常 |
| 17 | LOWERTOP RULE-SET Telegram.list | [blackmatrix7/ios_rule_script](https://github.com/blackmatrix7/ios_rule_script) | [Telegram.list](https://github.com/blackmatrix7/ios_rule_script/blob/master/rule/Shadowrocket/Telegram/Telegram.list) | 24 | 正常 |
| 18 | LOWERTOP RULE-SET PayPal.list | [blackmatrix7/ios_rule_script](https://github.com/blackmatrix7/ios_rule_script) | [PayPal.list](https://github.com/blackmatrix7/ios_rule_script/blob/master/rule/Shadowrocket/PayPal/PayPal.list) | 246 | 正常 |
| 19 | LOWERTOP RULE-SET Twitter.list | [blackmatrix7/ios_rule_script](https://github.com/blackmatrix7/ios_rule_script) | [Twitter.list](https://github.com/blackmatrix7/ios_rule_script/blob/master/rule/Shadowrocket/Twitter/Twitter.list) | 26 | 正常 |
| 20 | LOWERTOP RULE-SET Facebook.list | [blackmatrix7/ios_rule_script](https://github.com/blackmatrix7/ios_rule_script) | [Facebook.list](https://github.com/blackmatrix7/ios_rule_script/blob/master/rule/Shadowrocket/Facebook/Facebook.list) | 544 | 正常 |
| 21 | LOWERTOP RULE-SET Amazon.list | [blackmatrix7/ios_rule_script](https://github.com/blackmatrix7/ios_rule_script) | [Amazon.list](https://github.com/blackmatrix7/ios_rule_script/blob/master/rule/Shadowrocket/Amazon/Amazon.list) | 178 | 正常 |
| 22 | LOWERTOP RULE-SET Sony.list | [blackmatrix7/ios_rule_script](https://github.com/blackmatrix7/ios_rule_script) | [Sony.list](https://github.com/blackmatrix7/ios_rule_script/blob/master/rule/Shadowrocket/Sony/Sony.list) | 116 | 正常 |
| 23 | LOWERTOP RULE-SET Nintendo.list | [blackmatrix7/ios_rule_script](https://github.com/blackmatrix7/ios_rule_script) | [Nintendo.list](https://github.com/blackmatrix7/ios_rule_script/blob/master/rule/Shadowrocket/Nintendo/Nintendo.list) | 125 | 正常 |
| 24 | LOWERTOP RULE-SET Epic.list | [blackmatrix7/ios_rule_script](https://github.com/blackmatrix7/ios_rule_script) | [Epic.list](https://github.com/blackmatrix7/ios_rule_script/blob/master/rule/Shadowrocket/Epic/Epic.list) | 15 | 正常 |
| 25 | LOWERTOP RULE-SET SteamCN.list | [blackmatrix7/ios_rule_script](https://github.com/blackmatrix7/ios_rule_script) | [SteamCN.list](https://github.com/blackmatrix7/ios_rule_script/blob/master/rule/Shadowrocket/SteamCN/SteamCN.list) | 17 | 正常 |
| 26 | LOWERTOP RULE-SET Steam.list | [blackmatrix7/ios_rule_script](https://github.com/blackmatrix7/ios_rule_script) | [Steam.list](https://github.com/blackmatrix7/ios_rule_script/blob/master/rule/Shadowrocket/Steam/Steam.list) | 54 | 正常 |
| 27 | LOWERTOP RULE-SET Game.list | [blackmatrix7/ios_rule_script](https://github.com/blackmatrix7/ios_rule_script) | [Game.list](https://github.com/blackmatrix7/ios_rule_script/blob/master/rule/Shadowrocket/Game/Game.list) | 550 | 正常 |
| 28 | LOWERTOP RULE-SET GitHub.list | [blackmatrix7/ios_rule_script](https://github.com/blackmatrix7/ios_rule_script) | [GitHub.list](https://github.com/blackmatrix7/ios_rule_script/blob/master/rule/Shadowrocket/GitHub/GitHub.list) | 30 | 正常 |
| 29 | LOWERTOP RULE-SET Microsoft.list | [blackmatrix7/ios_rule_script](https://github.com/blackmatrix7/ios_rule_script) | [Microsoft.list](https://github.com/blackmatrix7/ios_rule_script/blob/master/rule/Shadowrocket/Microsoft/Microsoft.list) | 657 | 正常 |
| 30 | LOWERTOP RULE-SET Google.list | [blackmatrix7/ios_rule_script](https://github.com/blackmatrix7/ios_rule_script) | [Google.list](https://github.com/blackmatrix7/ios_rule_script/blob/master/rule/Shadowrocket/Google/Google.list) | 685 | 正常 |
| 31 | LOWERTOP RULE-SET TikTok.list | [blackmatrix7/ios_rule_script](https://github.com/blackmatrix7/ios_rule_script) | [TikTok.list](https://github.com/blackmatrix7/ios_rule_script/blob/master/rule/Shadowrocket/TikTok/TikTok.list) | 32 | 正常 |
| 32 | LOWERTOP RULE-SET Global.list | [blackmatrix7/ios_rule_script](https://github.com/blackmatrix7/ios_rule_script) | [Global.list](https://github.com/blackmatrix7/ios_rule_script/blob/master/rule/QuantumultX/Global/Global.list) | 35,791 | 正常 |
| 33 | LOWERTOP lazy.conf 内联 PROXY | [LOWERTOP/Shadowrocket](https://github.com/LOWERTOP/Shadowrocket) | [lazy.conf](https://github.com/LOWERTOP/Shadowrocket/blob/main/lazy.conf) | 3 | 正常 |

有效域名数为从该文件解析出的合法域名条数（含与其他来源重叠的部分）。LOWERTOP 的规则集由 lazy.conf 中所有 `RULE-SET ...,PROXY` 动态解析，Johnshall 只取策略为 Proxy 的规则，lazy.conf 变化时来源会随之增减。

## 处理规则

- gfwlist 先 Base64 解码，按 AutoProxy 语法取主机名，跳过 @@ 白名单和正则
- 去掉开头的点和 full: / domain: / +. 前缀
- 丢弃 regexp: / keyword: / DOMAIN-KEYWORD / IP-CIDR / GEOIP / USER-AGENT 等非域名规则
- 统一小写，校验域名格式（需含点，排除纯 IP），去重
- 与 [china-direct-domain](https://github.com/passionsu-su/china-direct-domain) 完整版完全相同的域名会被剔除（本次 2,007 条）
- 精简版：父域名已收录时去掉其子域名
- raw.githubusercontent.com 下载失败时自动改用 jsDelivr 镜像，仍失败的来源 15 秒后重试一次
- 某个来源失败时用其余来源继续，失败项写入 stats.json；总数少于 20,000 时本次不提交
