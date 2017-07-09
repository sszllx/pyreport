#include "extractorjson.h"

#include <QCoreApplication>
#include <QDebug>
#include <QDir>
#include <QFile>
#include <QJsonDocument>
#include <QJsonObject>
#include <QTime>
#include <QTimer>
#include <QTextCodec>

ExtractorJson::ExtractorJson(QObject *parent) : QObject(parent)
{
    bloom_parameters parameters;
    parameters.projected_element_count = 10000000;
    parameters.false_positive_probability = 0.00000001;
    parameters.random_seed = 0xA5A5A5A5;

    parameters.compute_optimal_parameters();
    bf = new bloom_filter(parameters);
}

void ExtractorJson::startParse()
{
    QString cur_dir = QCoreApplication::applicationDirPath() + "/ioslogs/";
    qDebug() << "cur dir:" << cur_dir;
    QDir dir(cur_dir);
    QStringList filter;
    filter << "*.log";
    QFileInfoList list = dir.entryInfoList(filter, QDir::Files);

    for (int i = 0; i < list.size(); ++i) {
        QFileInfo fileInfo = list.at(i);
        qDebug() << fileInfo.absoluteFilePath();
        parse(fileInfo.absoluteFilePath());
        QFile file(fileInfo.absoluteFilePath());
        file.remove();
    }

    QTimer::singleShot(1000*60*15, this, &ExtractorJson::startParse);
}

void ExtractorJson::parse(QString filename)
{
    QFile infile(filename);
    QString out_filename;

    out_filename = filename.replace(".log", ".id");
    QFile outfile(out_filename);
    QTextStream out(&outfile);

    if (!infile.open(QIODevice::ReadOnly | QIODevice::Text)) {
        qDebug() << "infile open failed";
        return;
    }

    if (!outfile.open(QIODevice::WriteOnly | QIODevice::Text)) {
        qDebug() << "outfile open failed";
        return;
    }

    QStringList idlist;

    int counter = 0;

    while (!infile.atEnd()) {
        QString line = infile.readLine().trimmed();
        counter++;

        int index = line.indexOf("{");
        int s_index = index;
        int e_index = index;
        QString jsonStr = line.mid(index, line.size());

        QString publisher = "null";
        QString adx = "null";
        index = jsonStr.indexOf("adx", s_index);
        if (index > 0) {
            index += 5;
            adx = jsonStr.mid(index, 1);
        }
//        qDebug() << "adx:" << adx;

        QString name = "null";
        index = jsonStr.indexOf("app", s_index);
        index = jsonStr.indexOf("name", index);
        if (index > 0) {
            index += 7;
            e_index = jsonStr.indexOf(",", index);
            name = jsonStr.mid(index, e_index - index - 2);
        }
//        qDebug() << "name:" << name;

        QString localtime = "null";
        index = jsonStr.indexOf("localtime", s_index);
        if (index > 0) {
            index += 12;
            e_index = jsonStr.indexOf(":", index);
            localtime = jsonStr.mid(index, e_index - index);
        }
//        qDebug() << "localtime:" << localtime;

        QString id = "null";
        index = jsonStr.indexOf("idfa", s_index);
        if (index > 0) {
            index += 7;
            e_index = jsonStr.indexOf(",", index);
            id = jsonStr.mid(index, e_index - index - 1);
        } else {
            index = jsonStr.indexOf("ifa", s_index);
            if (index > 0) {
                index += 6;
                e_index = jsonStr.indexOf(",", index);
                id = jsonStr.mid(index, e_index - index - 1);
            }
        }
//        qDebug() << "idfa:" << id;

        QString ua = "null";
        index = jsonStr.indexOf("ua", s_index);
        if (index > 0) {
            index += 5;
            e_index = jsonStr.indexOf("\",", index);
            ua = jsonStr.mid(index, e_index - index);
        }
//        qDebug() << "ua:" << ua;

#if 0
        QJsonParseError error;
        QJsonDocument jd = QJsonDocument::fromJson(jsonStrUtf8.toUtf8(), &error);
        // QJsonDocument jd = QJsonDocument::fromJson(jsonStr, &error);
        if (error.error != QJsonParseError::NoError) {
            qDebug() << "error:" << error.errorString() << " offset:" << error.offset;
            continue;
        }

        QJsonObject jo = jd.object();
        QJsonObject josub = jo.value("app").toObject();
        // app.publisher
        QJsonObject pub_obj = josub.value("publisher").toObject();
        QString publisher = pub_obj.value("id").toString();
        if (publisher.size() == 0) {
            publisher = "null";
        }
        // app.name
        QString name = josub.value("name").toString();
        if (name.size() == 0) {
            name = "null";
        }

        // qDebug() << name;
//        if (name.contains("头条")) {
//            toutiao++;
//            // qDebug() << "toutiao counter:" << toutiao;
//            continue;
//        }

        // adx
        int adx = -1;
        adx = jo.value("adx").toInt();

        // localtime
        QString localtime = jo.value("localtime").toString();
        if (localtime.size() == 0) {
            localtime = "null";
        }

        // idfa
        josub = jo.value("device").toObject();
        QString id = josub.value("idfa").toString();
        if (id.size() == 0) {
            id = josub.value("ifa").toString();
        }

        if (id.size() == 0) {
            id = "null";
        }

        // ip
        QString ip = josub.value("ip").toString();
        if (ip.size() == 0) {
            ip = "null";
        }

        // ua
        QString ua = josub.value("ua").toString();
        if (ua.size() == 0) {
            ua = "null";
        }

        // geo
        QJsonObject geo_obj = josub.value("geo").toObject();
        double geo_lon = -1;
        double geo_lat = -1;
        if (!geo_obj.isEmpty()) {
            geo_lon = geo_obj.value("lon").toDouble();
            geo_lat = geo_obj.value("lat").toDouble();
        }

#endif
        out << id << "\t"
            << name << "\t" << adx << "\t"
            << localtime << "\t" << ua << "\n";
    }
}
