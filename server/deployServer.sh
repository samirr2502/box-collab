while getopts k:h:s: flag
do
    case "${flag}" in
        k) key=${OPTARG};;
        h) hostname=${OPTARG};;
    esac
done

if [[ -z "$key" || -z "$hostname" ]]; then
    printf "\nMissing required parameter.\n"
    printf "  syntax: deployServer.sh -k <pem key file> -h <hostname>\n\n"
    exit 1
fi
service="box-collab"

printf "\n----> Deploying $service to $hostname with $key\n"

# Step 1
# printf "\n----> Build the distribution package\n"
# rm -rf dist
# mkdir dist
# cp -r src/* dist
# cp *.json dist

# Step 2
printf "\n----> Clearing out previous distribution on the target\n"
ssh -i "$key" ec2-user@$hostname << ENDSSH
rm -rf services/${service}
mkdir -p services/${service}
ENDSSH

# Step 3
printf "\n----> Copy the distribution package to the target\n"
scp -r -i "$key" ./* ec2-user@$hostname:services/$service

# Step 4
# printf "\n----> Deploy the service on the target\n"
# ssh -i "$key" ec2-user@$hostname << ENDSSH
# # bash -i
# # cd services/${service}
# # npm install
# # pm2 restart ${service}
# ENDSSH

# Step 5
# printf "\n----> Removing local copy of the distribution package\n"
# rm -rf dist
