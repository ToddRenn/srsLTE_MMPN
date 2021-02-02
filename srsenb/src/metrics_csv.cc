/*
 * Copyright 2013-2020 Software Radio Systems Limited
 *
 * This file is part of srsLTE.
 *
 * srsLTE is free software: you can redistribute it and/or modify
 * it under the terms of the GNU Affero General Public License as
 * published by the Free Software Foundation, either version 3 of
 * the License, or (at your option) any later version.
 *
 * srsLTE is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU Affero General Public License for more details.
 *
 * A copy of the GNU Affero General Public License can be found in
 * the LICENSE file in the top-level directory of this distribution
 * and at http://www.gnu.org/licenses/.
 *
 */

#include "srsenb/hdr/metrics_csv.h"

#include <float.h>
#include <iomanip>
#include <iostream>
#include <math.h>
#include <sstream>
#include <stdlib.h>
#include <unistd.h>

#include <stdio.h>

using namespace std;

namespace srsenb {

metrics_csv::metrics_csv(std::string filename) : n_reports(0), metrics_report_period(1.0), enb(NULL)
{
  file.open(filename.c_str(), std::ios_base::out);
}

metrics_csv::~metrics_csv()
{
  stop();
}

void metrics_csv::set_handle(enb_metrics_interface* enb_)
{
  enb = enb_;
}

void metrics_csv::stop()
{
  if (file.is_open()) {
    file << "#eof\n";
    file.flush();
    file.close();
  }
}

void metrics_csv::set_metrics(const enb_metrics_t& metrics, const uint32_t period_usec)
{
  if (file.is_open() && enb != NULL) {
    if (n_reports == 0 || n_reports > 10) {
      file << "------DL--------------------------------UL------------------------------------" << "\n";
      file << "rnti cqi  ri mcs brate   ok  nok  (%)  snr  phr mcs brate   ok  nok  (%)   bsr" << "\n";
    }

    for (int i = 0; i < metrics.stack.rrc.n_ues; i++) {
    if (metrics.stack.mac[i].tx_errors > metrics.stack.mac[i].tx_pkts) {
      printf("tx caution errors %d > %d\n", metrics.stack.mac[i].tx_errors, metrics.stack.mac[i].tx_pkts);
    }
    if (metrics.stack.mac[i].rx_errors > metrics.stack.mac[i].rx_pkts) {
      printf("rx caution errors %d > %d\n", metrics.stack.mac[i].rx_errors, metrics.stack.mac[i].rx_pkts);
    }

    file << int_to_hex_string(metrics.stack.mac[i].rnti, 4) << " ";
    file << float_to_string(SRSLTE_MAX(0.1, metrics.stack.mac[i].dl_cqi), 1, 3);
    file << float_to_string(metrics.stack.mac[i].dl_ri, 1, 4);
    if (not isnan(metrics.phy[i].dl.mcs)) {
      file << float_to_string(SRSLTE_MAX(0.1, metrics.phy[i].dl.mcs), 1, 4);
    } else {
      file << float_to_string(0, 2, 4);
    }
    if (metrics.stack.mac[i].tx_brate > 0) {
      file << float_to_eng_string(
          SRSLTE_MAX(0.1, (float)metrics.stack.mac[i].tx_brate / (metrics.stack.mac[i].nof_tti * 1e-3)), 1)
    } else {
      file << float_to_string(0, 1, 6) << "";
    }
    file << std::setw(5) << metrics.stack.mac[i].tx_pkts - metrics.stack.mac[i].tx_errors;
    file << std::setw(5) << metrics.stack.mac[i].tx_errors;
    if (metrics.stack.mac[i].tx_pkts > 0 && metrics.stack.mac[i].tx_errors) {
      file << float_to_string(
                  SRSLTE_MAX(0.1, (float)100 * metrics.stack.mac[i].tx_errors / metrics.stack.mac[i].tx_pkts), 1, 4) << "%";
    } else {
     file << float_to_string(0, 1, 4) << "%"; 
    }
    file << " ";

    if (not isnan(metrics.phy[i].ul.sinr)) {
      file << float_to_string(SRSLTE_MAX(0.1, metrics.phy[i].ul.sinr), 2, 4);
    } else {
      file << float_to_string(0, 1, 4);
    }

    file << float_to_string(metrics.stack.mac[i].phr, 2, 5);
    if (not isnan(metrics.phy[i].ul.mcs)) {
      file << float_to_string(SRSLTE_MAX(0.1, metrics.phy[i].ul.mcs), 1, 4);
    } else {
      file << float_to_string(0, 1, 4);
    }
    if (metrics.stack.mac[i].rx_brate > 0) {
      file << float_to_eng_string(
          SRSLTE_MAX(0.1, (float)metrics.stack.mac[i].rx_brate / (metrics.stack.mac[i].nof_tti * 1e-3)), 1);
    } else {
      file << float_to_string(0, 1) << "";
    }
    file << std::setw(5) << metrics.stack.mac[i].rx_pkts - metrics.stack.mac[i].rx_errors;
    file << std::setw(5) << metrics.stack.mac[i].rx_errors;

    if (metrics.stack.mac[i].rx_pkts > 0 && metrics.stack.mac[i].rx_errors > 0) {
      file << float_to_string(
                  SRSLTE_MAX(0.1, (float)100 * metrics.stack.mac[i].rx_errors / metrics.stack.mac[i].rx_pkts), 1, 4) << "%";
    } else {
      file << float_to_string(0, 1, 4) << "%";
    }
    file << float_to_eng_string(metrics.stack.mac[i].ul_buffer, 2);
    file << "\n";

    n_reports++;
  } else {
    std::cout << "Error, couldn't write CSV file." << std::endl;
  }
}

std::string metrics_csv::float_to_string(float f, int digits, bool add_semicolon)
{
  std::ostringstream os;
  const int          precision = (f == 0.0) ? digits - 1 : digits - log10f(fabs(f)) - 2 * DBL_EPSILON;
  os << std::fixed << std::setprecision(precision) << f;
  if (add_semicolon)
    os << ';';
  return os.str();
}

} // namespace srsenb
