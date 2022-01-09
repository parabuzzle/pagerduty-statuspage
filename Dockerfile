FROM python:3.7

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

ENV PDSTATUS_PD_URL=setme.pagerduty.com
ENV PDSTATUS_API_KEY=setme

COPY . .

CMD [ "gunicorn", "--bind=0.0.0.0", "pdstatus:create_app()" ]