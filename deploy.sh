#!/bin/bash

set -e

export HELM_RELEASE=conditioning-for-precise-visual-generative-ai-helm
export HELM_VERSION=1.1.0
export HELM_CHART_PATH=./helm
export IMAGE_PULL_SECRET=conditioningpullsecret

# Check if the image pull secret exists, and create it if it doesn't
if ! microk8s kubectl get secret "$IMAGE_PULL_SECRET" &>/dev/null; then
  export DOCKER_API_UNAME="${DOCKER_API_UNAME:-\$oauthtoken}"
  export DOCKER_REPO="${DOCKER_REPO:-nvcr.io}"
  # export DOCKER_API_KEY=...

  if [ -z "$DOCKER_API_KEY" ]; then
    echo "Env variable DOCKER_API_KEY is not set. Please set it for docker image pull secret creation."
    exit 1
  fi

  echo "Creating image pull secret..."
  microk8s kubectl create secret docker-registry $IMAGE_PULL_SECRET \
    --docker-server=$DOCKER_REPO \
    --docker-username=$DOCKER_API_UNAME \
    --docker-password=$DOCKER_API_KEY
else
  echo "Image pull secret '$IMAGE_PULL_SECRET' already exists."
fi

# Install Helm Chart from local files
export HELM_CHART_FILE=$HELM_RELEASE-$HELM_VERSION.tgz

# Check if the Helm release exists and uninstall it if it does
microk8s helm status $HELM_RELEASE &&
microk8s helm uninstall \
  $HELM_RELEASE

echo "Packaging Helm chart..."
microk8s helm3 package $HELM_CHART_PATH
mv ./$HELM_CHART_FILE $HELM_CHART_PATH/$HELM_CHART_FILE

echo "Installing Helm chart..."
microk8s helm install \
  $HELM_RELEASE \
  $HELM_CHART_PATH/$HELM_CHART_FILE \
  --set global.imagePullSecretName=$IMAGE_PULL_SECRET \
  --wait

echo "Installation completed."
echo "Use the following URL to launch the blueprint:"
echo "http://$(microk8s kubectl get svc playground -o jsonpath='{.spec.clusterIP}'):3000/?server=$(microk8s kubectl get svc streamer -o jsonpath='{.spec.clusterIP}')"
