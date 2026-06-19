
# BOUNDARYCAM Runtime API

## GET /healthz

Returns runtime health.

## POST /frames

Creates a hash-chained Boundary Frame.

## GET /frames

Lists stored frames.

## GET /frames/{frame_id}

Returns a frame by id.

## GET /chain/verify

Verifies hash-chain continuity.

## GET /receipt

Returns a runtime receipt containing frame count, head hash, and chain validity.
