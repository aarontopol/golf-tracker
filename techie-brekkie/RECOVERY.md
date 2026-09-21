# Techie Brekkie — source recovery status

The Techie Brekkie webapp was built in a Claude Code Remote Control session
(Aug 30 – Sep 1, 2026) on a local machine and deployed to Vercel via CLI
(`vercel deploy --prod`), so the source was never pushed to a git repository.
This folder is a recovery of that source from the production deployment
`dpl_Bzduttho4cKzLrs6KLowT83zCair` (project `techie-brekkie`, Sep 1, 2026).

## Recovered byte-perfect (SHA-1 verified against the deployment)

Every file currently in this folder matches its deployment blob SHA-1 exactly.

## Still to recover (truncated by the API relay; exact blobs exist on Vercel)

| Path | Deployment SHA-1 |
| --- | --- |
| README.md | b7be6817e8c747b0c1dbe112d872555384bd219b |
| components/TopicCard.tsx | 1f3a6529cba62d7a7a8553eda1f3555c297faa34 |
| lib/store.ts | 67d185a882548c3e52e1516400e3d548b900a49b |
| lib/research.ts | bc171785011d2192224d67327b9f32b6a127051e |
| app/page.tsx | 63d248fe5e5c7098b66031ca9166edc05547eaa3 |
| app/add/page.tsx | ca87c76e44d375ac7dc11f7e2c94eaae48697b1d |
| app/pick/page.tsx | 556e8fd7d8a0b4ebda27bbd70c7c16bd461b64f1 |
| public/favicon → app/favicon.ico | 9ecfcc8f0ead0bf3d2d7c39e084b88f41cc89a2e |
| public/icon-192.png | bda8a685be707e9e567f64f28a6c8f907f9f83ee |
| public/icon-512.png | fe84c0e2fde3c8ec67b4d8515c1e2712853f2ea3 |
| public/apple-touch-icon.png | 521f6ee5e2f6db98d300ffdffdd65aa339ef5070 |
| package-lock.json | 66c89dd25b6e6228f9c9bdc3d1f19dcc65a894b9 |

Not present in any listing (nested too deep for the relay, no SHA known):
`app/api/topics/route.ts` and `app/api/topics/[id]/route.ts` — to be
reconstructed from the recovered client code and `lib/store.ts` once pulled.

## Recovery deployment

A temporary helper project `techie-brekkie-recovery`
(deployment `dpl_AFMUi8KiK8Dmzvp5SCJazgCPXCG5`) references the blobs above and
serves them in small chunks through a key-protected function, sidestepping the
relay's response-size cap. Delete the `techie-brekkie-recovery` project from
the Vercel dashboard once recovery is complete. The production
`techie-brekkie` project was not modified.
