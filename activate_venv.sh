#! /bin/bash

echo "Karibu $USER, you are logged into $(hostname) on $(date)"

ls -l

pwd

cd project/ || { echo "Failed to change directory to 'project/'"; exit 1; }

if [[ -f ".scraper_venv/bin/activate" ]]; then
   source .scraper_venv/bin/activate
else
   echo "Venv activation script not found"
    exit 1
fi

## Navigate to the playwright_real_estate_scraper directory
cd playwright_real_estate_scraper || { echo "Failed to change directory to '/project/playwright_real_estate_scraper'"; exit 1; }

echo "Nime activate venv and moved to '/project/playwright_real_estate_scraper' wacha ni nicheki if docker inarun"

sleep  2

echo "........."
echo "...."

docker ps

#docker logs -f face07e9f063

echo "Unataka kucheki the logs of your scraper $USER? (Y/N)"
read -r user_input

#user_input=$(echo "$user_input" | tr '[:upper:]' '[:lower:]')
user_input=$(echo "$user_input" | tr -d '[:space:]' | tr '[:lower:]' '[:upper:]')


if [ "$user_input" == "Y" ]; then

    echo "Fetching logs for container face07e9f063..."

    sleep 2

    docker logs -f face07e9f063

elif [ "$user_input" == "N" ]; then
    echo "wacha tuache story ya logs we fanya mambo yako."
else
    echo "Invalid input. Please enter 'yes' or 'no'."
fi






