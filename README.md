### Co-WIN slots info Discord Update

Fetches available slots and posts to Discord. Core work by [Sengupta](https://gist.github.com/sengupta/dec88f899f239d86d32ab0e1c71ef7b1), with little massaging to adapt to Lambda

### Creating the Lambda

Create an empty Lambda from the UI with Python as the runtime. 

### Updating the Lambda

- Install [GNU Make](https://www.gnu.org/software/make/)
- Run `make all`
  - If you have profiles, make sure to export `export AWS_PROFILE=<name>`

### Environment Variables

Currently, two environment variables have been set:

- `DISCORD_WEBHOOK`: Discord Webhook to which to post the results
- `DISTRICT_ID`: District id to fetch the available slots.

These are created/updated manually. 
