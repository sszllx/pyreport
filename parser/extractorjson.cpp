#include "extractorjson.h"

#include <QCoreApplication>
#include <QDebug>
#include <QDir>
#include <QFile>
#include <QJsonDocument>
#include <QJsonObject>
#include <QTime>
#include <QTimer>

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
        // file.remove();
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

    while (!infile.atEnd()) {
        QString line = infile.readLine();

        int index = line.indexOf("{");
        QString jsonStr = line.mid(index, line.size());

        QJsonParseError error;
        QJsonDocument jd = QJsonDocument::fromJson(jsonStr.toUtf8(), &error);
        if (error.error != QJsonParseError::NoError) {
            qDebug() << error.errorString();
            continue;
        }

        QJsonObject jo = jd.object();
        QJsonObject josub = jo.value("app").toObject();
        QString name = josub.value("name").toString();
        // qDebug() << name;
        if (name.contains("头条")) {
            continue;
        }

        josub = jo.value("device").toObject();
        QString id = josub.value("idfa").toString();
        if (id.size() == 0) {
            id = josub.value("ifa").toString();
        }

        if (id.size() == 0 ||
                id == "00000000-0000-0000-0000-000000000000") {
            continue;
        }

        if (idlist.contains(id)) {
            continue;
        }

        idlist << id;

        // qDebug() << "size:" << idlist.size();
#if 0
        if (bf->contains(id.toStdString().c_str())) {
//            qDebug() << id;
            continue;
        }

        bf->insert(id.toStdString().c_str());
#endif
        out << id << "\n";
    }
}
